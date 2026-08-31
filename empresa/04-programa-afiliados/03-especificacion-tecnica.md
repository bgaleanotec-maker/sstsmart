# Módulo de Aliados — especificación técnica

Escrita contra el código real de este repositorio: Flask con `app/models/`,
`app/tenancy.py` (`TenantMixin`, `current_empresa_id`) y `app/constants.py` para roles.

---

## 1. La decisión de diseño que hay que entender primero

**Los modelos de aliados NO llevan `TenantMixin`.**

`TenantMixin` filtra automáticamente por `empresa_id` en cada SELECT. Un aliado existe
**por encima** de los tenants: refiere a muchas empresas y ninguna de ellas es "su" tenant.
Si le pones el mixin, el aliado desaparece de las consultas en cuanto haya un tenant en
contexto, y las liquidaciones se calculan mal en silencio.

```
┌─────────────────────────────────────────────────────┐
│  Tablas GLOBALES (sin TenantMixin, sin RLS)         │
│  aliados · referidos · comisiones · liquidaciones   │
└───────────────────────┬─────────────────────────────┘
                        │ referidos.empresa_id (FK, sin filtro automático)
┌───────────────────────▼─────────────────────────────┐
│  Tablas por TENANT (TenantMixin + RLS en Postgres)  │
│  empresas · empleados · matriz_riesgos · …          │
└─────────────────────────────────────────────────────┘
```

**Consecuencia operativa:** toda consulta que cruce las dos zonas se hace **fuera del
contexto de tenant** (jobs, scripts, panel de administración), igual que hacen hoy los jobs
de escalamiento. Documéntalo en el módulo o alguien lo va a romper en seis meses.

**Y una regla de seguridad que se olvida:** el panel del aliado muestra empresas de
**otros** tenants. Nunca expongas por ahí datos operativos —empleados, exámenes, matrices—.
Solo: razón social, NIT parcial enmascarado, plan, estado y valor de la comisión.

---

## 2. Modelo de datos

`app/models/aliado.py`:

```python
"""Programa de Aliados — modelos GLOBALES.

IMPORTANTE: ninguno lleva TenantMixin. Un aliado cruza tenants por definición.
Ver empresa/04-programa-afiliados/03-especificacion-tecnica.md §1.
"""
from datetime import datetime, timedelta
from decimal import Decimal

from app import db


class Aliado(db.Model):
    __tablename__ = 'aliados'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(12), unique=True, nullable=False, index=True)

    # Identificación
    nombre = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(10), nullable=False)   # CC | NIT | CE
    documento = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))

    # Perfil comercial
    profesion = db.Column(db.String(120))
    licencia_sst = db.Column(db.String(60))
    empresas_atendidas = db.Column(db.Integer)

    # Datos tributarios — determinan la liquidación. Ver §6.
    responsable_iva = db.Column(db.Boolean, default=False, nullable=False)
    declarante_renta = db.Column(db.Boolean, default=False, nullable=False)
    obligado_facturar = db.Column(db.Boolean, default=False, nullable=False)

    # Pago
    banco = db.Column(db.String(80))
    tipo_cuenta = db.Column(db.String(20))          # ahorros | corriente
    numero_cuenta = db.Column(db.String(40))        # cifrar en reposo

    # Estado
    estado = db.Column(db.String(20), default='activo', nullable=False)
    # activo | inactivo | suspendido | terminado
    nivel = db.Column(db.String(20), default='aliado', nullable=False)
    # aliado (20%) | senior (25%)

    # Prueba de aceptación del contrato — ver empresa/04-.../02-contrato
    contrato_version = db.Column(db.String(10))
    contrato_hash = db.Column(db.String(64))
    contrato_aceptado_en = db.Column(db.DateTime)
    contrato_ip = db.Column(db.String(45))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    terminado_en = db.Column(db.DateTime)

    referidos = db.relationship('Referido', back_populates='aliado', lazy='dynamic')

    PORCENTAJES = {'aliado': Decimal('0.20'), 'senior': Decimal('0.25')}
    PORCENTAJE_PERMANENCIA = Decimal('0.10')
    MESES_COLA_TRAS_TERMINACION = 24

    def porcentaje_lanzamiento(self):
        return self.PORCENTAJES.get(self.nivel, Decimal('0.20'))

    def puede_devengar(self, fecha=None):
        """Contrato cl. 9.4 y 9.5: el aliado inactivo conserva las comisiones de
        permanencia, y el terminado SIN CULPA las conserva 24 meses. Solo el
        suspendido y el terminado por incumplimiento dejan de devengar."""
        if self.estado in ('activo', 'inactivo'):
            return True
        if self.estado == 'terminado' and self.terminado_en:
            fecha = fecha or datetime.utcnow()
            return fecha <= self.terminado_en + timedelta(days=30 * self.MESES_COLA_TRAS_TERMINACION)
        return False

    def clientes_activos(self):
        return self.referidos.filter_by(estado='activo').count()

    def evaluar_nivel(self):
        """Sube a senior con 10 clientes activos. No baja: el nivel ganado no se
        quita, porque quitarlo destruye la confianza en el programa."""
        if self.nivel == 'aliado' and self.clientes_activos() >= 10:
            self.nivel = 'senior'


class Referido(db.Model):
    """Vínculo aliado ↔ empresa. Uno por empresa referida, para siempre."""
    __tablename__ = 'referidos'
    __table_args__ = (
        db.UniqueConstraint('empresa_id', name='uq_referido_empresa'),
        db.Index('ix_referidos_aliado_estado', 'aliado_id', 'estado'),
    )

    id = db.Column(db.Integer, primary_key=True)
    aliado_id = db.Column(db.Integer, db.ForeignKey('aliados.id'), nullable=False, index=True)

    # NIT reservado antes de que exista la empresa en el sistema
    nit_reservado = db.Column(db.String(20), index=True)
    reservado_en = db.Column(db.DateTime)
    reserva_vence_en = db.Column(db.DateTime)

    # Se llena cuando la empresa efectivamente se registra
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), index=True)

    origen = db.Column(db.String(20), nullable=False)   # registro_previo | enlace
    estado = db.Column(db.String(20), default='reservado', nullable=False)
    # reservado | vencido | activo | mora | cancelado

    # Contrato cl. 5.3: el 25% de nivel senior aplica solo a los referidos NUEVOS.
    # Se congela aqui al primer pago; no se lee del nivel actual del aliado.
    porcentaje_lanzamiento = db.Column(db.Numeric(5, 4))

    primer_pago_en = db.Column(db.DateTime)     # inicia el reloj de los 12 meses
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    aliado = db.relationship('Aliado', back_populates='referidos')

    DIAS_RESERVA = 90

    def reservar(self):
        self.reservado_en = datetime.utcnow()
        self.reserva_vence_en = self.reservado_en + timedelta(days=self.DIAS_RESERVA)

    def porcentaje_vigente(self, fecha=None):
        """20% (o 25% si senior) los primeros 12 meses desde el primer pago; 10% después."""
        if not self.primer_pago_en:
            return Decimal('0')
        fecha = fecha or datetime.utcnow()
        meses = (fecha.year - self.primer_pago_en.year) * 12 + (fecha.month - self.primer_pago_en.month)
        if meses < 12:
            # congelado al primer pago; nunca se recalcula desde el nivel actual
            return self.porcentaje_lanzamiento or Aliado.PORCENTAJES['aliado']
        return Aliado.PORCENTAJE_PERMANENCIA


class Comision(db.Model):
    """Una comisión por cada pago recibido de un cliente referido."""
    __tablename__ = 'comisiones'
    __table_args__ = (
        db.UniqueConstraint('pago_id', name='uq_comision_pago'),   # idempotencia
        db.Index('ix_comisiones_aliado_estado', 'aliado_id', 'estado'),
    )

    id = db.Column(db.Integer, primary_key=True)
    aliado_id = db.Column(db.Integer, db.ForeignKey('aliados.id'), nullable=False, index=True)
    referido_id = db.Column(db.Integer, db.ForeignKey('referidos.id'), nullable=False)
    pago_id = db.Column(db.Integer, db.ForeignKey('pagos.id'), nullable=False)

    base = db.Column(db.Numeric(14, 2), nullable=False)        # valor pagado SIN IVA
    porcentaje = db.Column(db.Numeric(5, 4), nullable=False)   # se congela al causar
    valor = db.Column(db.Numeric(14, 2), nullable=False)

    periodo = db.Column(db.String(7), nullable=False, index=True)   # 'YYYY-MM'
    estado = db.Column(db.String(20), default='causada', nullable=False)
    # causada | liquidada | pagada | reversada | suspendida

    liquidacion_id = db.Column(db.Integer, db.ForeignKey('liquidaciones.id'), index=True)
    causada_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reversada_en = db.Column(db.DateTime)
    motivo_reversion = db.Column(db.String(255))


class Liquidacion(db.Model):
    """Agrupa las comisiones de un aliado en un periodo. Es lo que se paga."""
    __tablename__ = 'liquidaciones'
    __table_args__ = (
        db.UniqueConstraint('aliado_id', 'periodo', name='uq_liquidacion_aliado_periodo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    aliado_id = db.Column(db.Integer, db.ForeignKey('aliados.id'), nullable=False, index=True)
    periodo = db.Column(db.String(7), nullable=False)

    subtotal = db.Column(db.Numeric(14, 2), nullable=False)
    iva = db.Column(db.Numeric(14, 2), default=0, nullable=False)
    retefuente = db.Column(db.Numeric(14, 2), default=0, nullable=False)
    reteica = db.Column(db.Numeric(14, 2), default=0, nullable=False)   # ver §6
    total_a_pagar = db.Column(db.Numeric(14, 2), nullable=False)

    # Datos bancarios congelados al aprobar: un cambio de cuenta posterior no
    # redirige un pago ya aprobado (ver §9)
    banco_snapshot = db.Column(db.String(80))
    cuenta_snapshot = db.Column(db.String(40))

    estado = db.Column(db.String(20), default='borrador', nullable=False)
    # borrador | aprobada | pagada | acumulada
    documento_soporte_cufe = db.Column(db.String(96))   # si el aliado no factura
    factura_aliado_num = db.Column(db.String(40))       # si el aliado factura

    generada_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    pagada_en = db.Column(db.DateTime)
    comprobante_url = db.Column(db.String(500))

    MINIMO_PAGO = Decimal('100000')
```

> **`UniqueConstraint('pago_id')` en `Comision` es la línea más importante del modelo.** Un
> webhook de pasarela **se reintenta**. Sin esa restricción, un reintento duplica la comisión
> y lo descubres cuando el aliado reclama —o peor, cuando no reclama.

---

## 3. Atribución

`app/services/aliados.py`:

```python
from datetime import datetime, timedelta

COOKIE_REF = 'ref_aliado'
DIAS_COOKIE = 90


def registrar_click_referido(response, codigo):
    """Se llama en el before_request cuando llega ?ref=CODIGO."""
    if not Aliado.query.filter_by(codigo=codigo, estado='activo').first():
        return response
    response.set_cookie(
        COOKIE_REF, codigo,
        max_age=DIAS_COOKIE * 24 * 3600,
        httponly=True, samesite='Lax', secure=True,
    )
    return response


def resolver_atribucion(nit, codigo_cookie=None):
    """Prelación: (1) reserva previa vigente por NIT, (2) cookie de enlace.

    Devuelve el Referido creado o vinculado, o None si la empresa no es referible.
    """
    if _es_o_fue_cliente(nit, meses=12):
        return None

    reserva = (Referido.query
               .filter_by(nit_reservado=nit, estado='reservado')
               .filter(Referido.reserva_vence_en >= datetime.utcnow())
               .order_by(Referido.reservado_en.asc())   # el primero en el tiempo
               .first())
    if reserva:
        return reserva

    if codigo_cookie:
        aliado = Aliado.query.filter_by(codigo=codigo_cookie, estado='activo').first()
        if aliado:
            ref = Referido(aliado_id=aliado.id, nit_reservado=nit, origen='enlace')
            ref.reservar()
            db.session.add(ref)
            return ref
    return None
```

**Reglas que hay que codificar y probar:**

| Regla | Prueba que la cubre |
|---|---|
| Reserva previa vence a cookie | `test_reserva_previa_gana_sobre_cookie` |
| Entre dos reservas del mismo NIT, gana la más antigua | `test_reserva_mas_antigua_gana` |
| Reserva vencida (>90 días) no atribuye | `test_reserva_vencida_no_atribuye` |
| Cliente actual o de los últimos 12 meses no es referible | `test_cliente_existente_no_es_referible` |
| Aliado suspendido no atribuye | `test_aliado_suspendido_no_atribuye` |
| Auto-referido (documento del aliado == NIT referido) se bloquea | `test_autoreferido_bloqueado` |

---

## 4. Causación de la comisión — en el webhook de pago

```python
def causar_comision(pago):
    """Se llama SOLO cuando el pago está confirmado por la pasarela.

    Idempotente por UniqueConstraint(pago_id): un webhook reintentado no duplica.
    """
    referido = Referido.query.filter_by(empresa_id=pago.empresa_id).first()
    if not referido or referido.estado in ('cancelado', 'vencido'):
        return None

    # El contrato (cl. 9.4 y 9.5) garantiza comisiones de permanencia al aliado
    # INACTIVO y al TERMINADO sin culpa, durante 24 meses. Excluir aquí a todo el
    # que no esté 'activo' incumpliría el contrato en silencio.
    if not referido.aliado.puede_devengar():
        return None

    if not referido.primer_pago_en:
        referido.primer_pago_en = pago.fecha       # arranca el reloj de los 12 meses
        referido.estado = 'activo'
        # congela el porcentaje ANTES de reevaluar el nivel: cl. 5.3 dice que el 25%
        # es para los referidos nuevos, no para los que ya estaban en curso
        referido.porcentaje_lanzamiento = referido.aliado.porcentaje_lanzamiento()
        referido.aliado.evaluar_nivel()

    base = pago.valor_sin_iva - pago.valor_consultoria   # la consultoría no comisiona
    if base <= 0:
        return None

    porcentaje = referido.porcentaje_vigente(pago.fecha)
    comision = Comision(
        aliado_id=referido.aliado_id,
        referido_id=referido.id,
        pago_id=pago.id,
        base=base,
        porcentaje=porcentaje,          # se congela: si mañana cambia el programa, esta no cambia
        valor=(base * porcentaje).quantize(Decimal('1')),
        periodo=pago.fecha.strftime('%Y-%m'),
    )
    db.session.add(comision)
    return comision


def reversar_comision(pago, motivo):
    """Devolución o chargeback."""
    c = Comision.query.filter_by(pago_id=pago.id).first()
    if c and c.estado in ('causada', 'liquidada'):
        c.estado = 'reversada'
        c.reversada_en = datetime.utcnow()
        c.motivo_reversion = motivo
```

> **Congelar el porcentaje en la fila es deliberado.** El contrato dice que un cambio de
> programa no afecta comisiones causadas. Si el porcentaje se recalculara al vuelo desde la
> configuración vigente, el sistema violaría el contrato sin que nadie lo note.

---

## 5. Job mensual de liquidación

`app/tasks/liquidar_comisiones.py`, programado el **día 10 de cada mes**:

```python
def liquidar_periodo(periodo):   # 'YYYY-MM'
    """Corre FUERA de contexto de tenant: cruza aliados con muchas empresas."""
    for aliado in Aliado.query.filter(Aliado.estado.in_(('activo', 'inactivo', 'terminado'))):
        if not aliado.puede_devengar():
            continue

        # Todas las comisiones aun no liquidadas, no solo las del periodo: las de
        # meses anteriores que no alcanzaron el minimo siguen en estado 'causada'
        # y deben LIQUIDARSE ahora, no volver a sumarse el mes entrante.
        comisiones = (Comision.query
                      .filter_by(aliado_id=aliado.id, estado='causada')
                      .filter(Comision.periodo <= periodo)      # 'YYYY-MM' ordena lexicograficamente
                      .all())
        if not comisiones:
            continue

        subtotal = sum(c.valor for c in comisiones)

        if subtotal < Liquidacion.MINIMO_PAGO:
            continue        # quedan en 'causada' y entran en el corte siguiente

        iva = subtotal * Decimal('0.19') if aliado.responsable_iva else Decimal('0')
        retefuente = _calcular_retefuente(aliado, subtotal)
        reteica = _calcular_reteica(aliado, subtotal)

        liq = Liquidacion(
            aliado_id=aliado.id, periodo=periodo,
            subtotal=subtotal, iva=iva, retefuente=retefuente, reteica=reteica,
            total_a_pagar=subtotal + iva - retefuente - reteica,
            banco_snapshot=aliado.banco, cuenta_snapshot=aliado.numero_cuenta,
            estado='borrador',
        )
        db.session.add(liq)
        db.session.flush()
        for c in comisiones:
            c.estado = 'liquidada'
            c.liquidacion_id = liq.id
    db.session.commit()
```

**Suspensión por mora del cliente:** un job diario marca `Referido.estado = 'mora'` cuando el
cliente lleva más de 60 días sin pagar, y las comisiones de ese referido no entran en la
liquidación hasta que vuelva a `activo`.

---

## 6. Retención en la fuente — el punto delicado

```python
def _calcular_retefuente(aliado, base):
    """Comisiones a personas naturales y jurídicas.

    [NE] Las tarifas deben confirmarse con el contador ANTES de la primera
    liquidación. Ver empresa/02-dian-y-facturacion/02-decision-iva-y-regimen.md §5.
    Parametrizar en base de datos, NUNCA en el código: cambian por decreto.
    """
    tarifa = ParametroTributario.vigente('retefuente_comisiones',
                                         persona=aliado.tipo_documento,
                                         declarante=aliado.declarante_renta)
    return (base * tarifa).quantize(Decimal('1'))
```

**Retención de ICA.** Siendo contribuyente de ICA en Bogotá y pagando comisiones por
servicios, es muy probable que también seas **agente de retención de ICA**, con base mínima
por servicios de **4 UVT = $209.496**. Por eso `Liquidacion` lleva la columna `reteica`.
**[NE] Confirma con tu contador si eres agente retenedor de ICA y a qué tarifa**, antes de la
primera liquidación; si no lo eres, deja la columna en cero y escribe por qué.

**Tabla `parametros_tributarios`** con vigencias (`vigente_desde`, `vigente_hasta`). El
Decreto 572 de 2025 fue suspendido en mayo de 2026 y reactivado en julio del mismo año: las
tarifas **cambiaron a mitad de año**. Un porcentaje escrito en el código es una bomba de
tiempo; una tabla con vigencias se corrige con un INSERT.

**Documento soporte.** Si `obligado_facturar == False`, hay que emitir **documento soporte en
adquisiciones a no obligados a facturar** por cada liquidación pagada, y guardar el CUFE en
`Liquidacion.documento_soporte_cufe`. Es requisito para que el gasto sea deducible. Verifica
que el proveedor de facturación elegido soporte ese documento por API →
[`../02-dian-y-facturacion/04-proveedores-comparativa.md`](../02-dian-y-facturacion/04-proveedores-comparativa.md) §4.

---

## 7. Rutas

`app/routes/aliados.py` — blueprint `aliados`, rol `ALIADO` en `app/constants.py`:

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/aliados/panel` | Resumen: clientes activos, comisión del mes, acumulado, nivel |
| GET/POST | `/aliados/prospectos` | Registrar NIT (reserva 90 días) y ver reservas vigentes |
| GET | `/aliados/referidos` | Lista: razón social, **NIT enmascarado**, plan, estado, comisión |
| GET | `/aliados/liquidaciones` | Histórico y descarga en PDF |
| GET | `/aliados/material` | Kit comercial descargable |
| GET/POST | `/aliados/perfil` | Datos de contacto, tributarios y bancarios |

**Admin** (`app/routes/admin_aliados.py`, rol `ADMIN`): aprobación de inscripciones,
resolución de disputas de atribución, generación y aprobación de liquidaciones, registro de
pagos, suspensión y terminación.

---

## 8. Orden de implementación

Cada paso es desplegable y no rompe lo anterior.

1. **Migración** de las cuatro tablas. Sin `TenantMixin`. Índices como están arriba.
2. **Captura del enlace `?ref=`** en `before_request` + cookie. Cuatro líneas, cero riesgo.
3. **Registro previo de NIT** y `resolver_atribucion` + los seis tests de §3.
4. **`causar_comision` en el webhook de pago.** Con la restricción única en `pago_id` desde el primer día.
5. **Panel del aliado** de solo lectura. Ya hay algo que mostrar.
6. **Job de liquidación** + `parametros_tributarios`.
7. **Integración con documento soporte** por API.
8. **Admin** de disputas y pagos.

**Bloqueadores previos:** los pasos 4 y 6 dependen de que exista el módulo de suscripciones y
pagos, que hoy no está (`docs/02-producto/01-diagnostico-producto-actual.md`, bloqueador 4).
Los pasos 1 a 3 y 5 **se pueden hacer ya**, y son suficientes para lanzar el programa con
liquidación manual durante los primeros meses. Con menos de veinte aliados, liquidar en una
hoja de cálculo es perfectamente razonable.

---

## 9. Riesgos técnicos

| Riesgo | Mitigación |
|---|---|
| Webhook duplicado → comisión doble | `UniqueConstraint('pago_id')` + `ON CONFLICT DO NOTHING` |
| Aliado ve datos de otro tenant | El panel solo consulta las cuatro tablas globales; nunca joins a tablas operativas |
| Cookie de referido sobrescrita por otro enlace | Última-visita gana, pero la reserva previa tiene prelación absoluta |
| Cambio de tarifas tributarias a mitad de año | `parametros_tributarios` con vigencias, nunca constantes en código |
| Job de liquidación corre dos veces | `UniqueConstraint('aliado_id', 'periodo')` |
| Aliado modifica su cuenta bancaria justo antes del pago | `banco_snapshot` y `cuenta_snapshot` congelados al aprobar la liquidación, y notificación por correo de todo cambio de cuenta |
| Comisión acumulada por no llegar al mínimo se suma dos veces | Las comisiones bajo el mínimo **permanecen en estado `causada`** y se liquidan todas juntas cuando se supera; nunca se suma un "saldo anterior" sobre filas que siguen abiertas |
| Aliado terminado pierde comisiones que el contrato le garantiza | `Aliado.puede_devengar()` implementa las cláusulas 9.4 y 9.5, y el job de liquidación lo respeta |
