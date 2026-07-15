from typing import Dict, List, Any
from plugin_sdk import PluginBase
from verbum_core import Evidencia, Inferencia, NivelAlerta

class CubaCore(PluginBase):
    """
    Plugin CubaCore — Normativa cubana para emprendedores y mipymes.
    """

    nombre: str = "CubaCore"
    dominio: str = "cuba"
    version: str = "0.1"
    tipos_evidencia_soportados: List[str] = [
        "creacion_mipyme", "operacion_tributaria", "precios", 
        "seguridad_social", "extincion", "sanciones", "seguridad_alimentaria",
        "medio_ambiente", "contratos_laborales", "cuentas_bancarias",
        "importacion_exportacion", "licencias_permisos"
    ]

    def __init__(self) -> None:
        super().__init__()
        
        # === NORMAS JURÍDICAS CODIFICADAS ===

        # Decreto-Ley 46/2021 — Creación y funcionamiento de MIPYMES
        self.normas_creacion: Dict[str, Any] = {
            "capital_minimo": 0,
            "socios_minimos": 1,
            "socios_maximos_micro": 10,
            "socios_maximos_pequena": 35,
            "socios_maximos_mediana": 100,
            "incompatibilidades": [
                "Ser socio de otra MIPYME",
                "Ser cuadro/funcionario del Estado (para privadas)",
                "Ocupar cargo electivo profesional en órgano estatal"
            ],
            "plazo_escritura_notarial": 30,
            "plazo_mep_respuesta": 5,
            "moneda_aporte": "CUP",
            "forma_juridica": "S.R.L.",
            "tipos_propiedad": ["privada", "estatal", "mixta"]
        }

        # Decreto-Ley 107/2025 — Modificaciones tributarias
        self.normas_tributarias: Dict[str, Any] = {
            "impuestos": {
                "utilidades": {"tipo": "sobre_utilidades", "tasa": "variable"},
                "ventas_servicios": {"tipo": "sobre_ventas", "tasa": 0.10},
                "ingresos_personales": {
                    "minimo_exento_anual": 39120,
                    "escala": [
                        {"hasta": 75000, "tasa": 0.03},
                        {"hasta": 150000, "tasa": 0.05},
                        {"hasta": 250000, "tasa": 0.10},
                        {"hasta": 350000, "tasa": 0.15},
                        {"hasta": float('inf'), "tasa": 0.20}
                    ]
                },
                "retencion_dividendos": 0.05,
            },
            "exenciones_primer_ano": True,
            "exencion_6_meses_reconversion": True,
            "contribucion_territorial_exencion_2_anos": True,
            "nit_obligatorio": True,
            "plazo_actualizacion_datos": 30,
            "frecuencia_pago_seguridad_social": "mensual",
            "frecuencia_pago_tcp": "trimestral",
        }

        # Precios
        self.normas_precios: Dict[str, Any] = {
            "fijacion_autonoma": True,
            "excepcion_aprobacion_centralizada": True,
            "limite_ganancia_sector_estatal": True,
            "multas_especulacion": True,
            "precios_abusivos_prohibidos": True,
        }

        # Seguridad alimentaria
        self.normas_seguridad_alimentaria: Dict[str, Any] = {
            "registro_sanitario_obligatorio": True,
            "normas_higiene_obligatorias": True,
            "trazabilidad_productos": True,
            "prohibicion_adulteracion": True,
        }

        # Medio ambiente
        self.normas_medio_ambiente: Dict[str, Any] = {
            "licencia_ambiental_obligatoria": True,
            "gestion_residuos_obligatoria": True,
            "zonas_protegidas_restricciones": True,
            "contribucion_restauracion_zonas": True,
        }

        # Extinción — Art. 45-53 Gaceta Oficial 2026-ES1
        self.normas_extincion: Dict[str, Any] = {
            "causales_baja": [
                "extincion", "escision", "absorcion", "fusion",
                "fallecimiento", "salida_definitiva_pais",
                "ausencia_presuncion_muerte", "privacion_libertad_mayor_3_meses",
                "conclusion_actividades_gravadas",
                "cierre_establecimientos_sancion", "retirada_licencia",
                "no_renovacion_licencia", "baja_seguridad_social"
            ],
            "documentos_requeridos": {
                "extincion": "disposicion_legal_cancelacion_registral",
                "fallecimiento": "certificacion_defuncion",
                "salida_pais": "certificacion_organo_estatal",
                "privacion_libertad": "copia_resolucion_judicial",
                "cierre_sancion": "resolucion_autoridad_facultada",
                "conclusion_actividades": "documento_organismo_rector"
            },
            "obligaciones_pendientes": True,
        }

        # Sanciones
        self.normas_sanciones: Dict[str, Any] = {
            "cierre_establecimientos": True,
            "retirada_licencia_comercial": True,
            "multas_precios": True,
            "multas_tributarias": True,
            "reincidencia_denegacion_creacion": True,
        }

        # Contratos laborales
        self.normas_laborales: Dict[str, Any] = {
            "contrato_escrito_obligatorio": True,
            "salario_minimo_estatal": True,
            "seguridad_social_obligatoria": True,
            "horas_extra_reguladas": True,
            "derecho_sindical": True,
        }

        # Importación/Exportación
        self.normas_comercio_exterior: Dict[str, Any] = {
            "autorizacion_mincex": True,
            "cuentas_divisas_permitidas": True,
            "aranceles_importacion": True,
            "beneficios_arancelarios_materias_primas": True,
            "exencion_productos_renovables": True,
        }

    def procesar(self, evidencia: Evidencia) -> Inferencia:
        tipo = evidencia.tipo.lower()
        datos = evidencia.contenido

        if tipo == "creacion_mipyme":
            return self._procesar_creacion(datos, evidencia.id)
        elif tipo == "operacion_tributaria":
            return self._procesar_tributaria(datos, evidencia.id)
        elif tipo == "precios":
            return self._procesar_precios(datos, evidencia.id)
        elif tipo == "seguridad_social":
            return self._procesar_seguridad_social(datos, evidencia.id)
        elif tipo == "extincion":
            return self._procesar_extincion(datos, evidencia.id)
        elif tipo == "sanciones":
            return self._procesar_sanciones(datos, evidencia.id)
        elif tipo == "seguridad_alimentaria":
            return self._procesar_seguridad_alimentaria(datos, evidencia.id)
        elif tipo == "medio_ambiente":
            return self._procesar_medio_ambiente(datos, evidencia.id)
        elif tipo == "contratos_laborales":
            return self._procesar_laboral(datos, evidencia.id)
        elif tipo == "cuentas_bancarias":
            return self._procesar_bancaria(datos, evidencia.id)
        elif tipo == "importacion_exportacion":
            return self._procesar_comercio_exterior(datos, evidencia.id)
        elif tipo == "licencias_permisos":
            return self._procesar_licencias(datos, evidencia.id)
        else:
            return Inferencia(
                tipo="alerta",
                descripcion=f"Tipo '{tipo}' no manejado por CubaCore",
                evidencias_usadas=[evidencia.id],
                nivel_alerta=NivelAlerta.GRIS,
                confianza=0.3,
                accion_recomendada="Verificar tipo de evidencia",
                plugin_origen=self.nombre
            )

    def _procesar_creacion(self, datos: Dict, evidencia_id: str) -> Inferencia:
        errores = []
        alertas = []

        num_socios = datos.get("numero_socios", 0)
        tipo_mipyme = datos.get("tipo_mipyme", "").lower()

        if tipo_mipyme == "micro" and num_socios > self.normas_creacion["socios_maximos_micro"]:
            errores.append(f"Microempresa excede límite de {self.normas_creacion['socios_maximos_micro']} ocupados (tiene {num_socios})")
        elif tipo_mipyme == "pequena" and num_socios > self.normas_creacion["socios_maximos_pequena"]:
            errores.append(f"Pequeña empresa excede límite de {self.normas_creacion['socios_maximos_pequena']} ocupados")
        elif tipo_mipyme == "mediana" and num_socios > self.normas_creacion["socios_maximos_mediana"]:
            errores.append(f"Mediana empresa excede límite de {self.normas_creacion['socios_maximos_mediana']} ocupados")

        es_funcionario = datos.get("es_funcionario_estado", False)
        es_socio_otra = datos.get("es_socio_otra_mipyme", False)
        es_cargo_electivo = datos.get("es_cargo_electivo", False)

        if es_funcionario and datos.get("tipo_propiedad") == "privada":
            errores.append("INCOMPATIBLE: Funcionario del Estado no puede ser socio de MIPYME privada (Art. 49 Decreto-Ley 46)")
        if es_socio_otra:
            errores.append("INCOMPATIBLE: No puede ser socio de más de una MIPYME (Art. 49 Decreto-Ley 46)")
        if es_cargo_electivo:
            errores.append("INCOMPATIBLE: Cargo electivo profesional incompatible con ser socio (Art. 49)")

        capital = datos.get("capital_social", 0)
        if capital < self.normas_creacion["capital_minimo"]:
            errores.append(f"Capital social insuficiente (mínimo: {self.normas_creacion['capital_minimo']} CUP)")

        moneda = datos.get("moneda_aporte", "")
        if moneda and moneda != "CUP":
            alertas.append(f"Aportes dinerarios deben ser en CUP (Art. 22 Decreto-Ley 46). Moneda declarada: {moneda}")

        dias_desde_aprobacion = datos.get("dias_desde_aprobacion_mep", 0)
        if dias_desde_aprobacion > self.normas_creacion["plazo_escritura_notarial"]:
            alertas.append(f"Plazo de {self.normas_creacion['plazo_escritura_notarial']} días hábiles para escritura notarial vencido (lleva {dias_desde_aprobacion})")

        es_reconversion = datos.get("es_reconversion_negocio_preexistente", False)
        tiene_incumplimientos = datos.get("tiene_incumplimientos_fiscales", False)
        if es_reconversion and tiene_incumplimientos:
            errores.append("RECONVERSIÓN DENEGADA: Reincidencia/multireincidencia en incumplimientos fiscales o bancarios (Art. 8 Res. 64/2021)")

        forma = datos.get("forma_juridica", "")
        if forma and "S.R.L" not in forma and "SRL" not in forma:
            alertas.append(f"Forma jurídica debe ser S.R.L. (Art. 11 Decreto-Ley 46). Declarada: {forma}")

        if errores:
            return Inferencia(
                tipo="decision",
                descripcion=f"CREACIÓN BLOQUEADA: {len(errores)} incumplimientos graves en requisitos de constitución",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.ROJO,
                confianza=1.0,
                accion_recomendada=f"NO PROCEDER con creación hasta resolver: {'; '.join(errores[:3])}",
                plugin_origen=self.nombre
            )
        elif alertas:
            return Inferencia(
                tipo="alerta",
                descripcion=f"CREACIÓN CON OBSERVACIONES: {len(alertas)} advertencias en requisitos",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.AMARILLO,
                confianza=0.85,
                accion_recomendada=f"Revisar antes de continuar: {'; '.join(alertas[:3])}",
                plugin_origen=self.nombre
            )
        else:
            return Inferencia(
                tipo="informe",
                descripcion="CREACIÓN VÁLIDA: Todos los requisitos de constitución cumplidos según Decreto-Ley 46/2021",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.VERDE,
                confianza=0.95,
                accion_recomendada="Proceder con escritura pública notarial e inscripción en Registro Mercantil",
                plugin_origen=self.nombre
            )

    def _procesar_tributaria(self, datos: Dict, evidencia_id: str) -> Inferencia:
        alertas = []
        errores = []

        tiene_nit = datos.get("tiene_nit", False)
        if not tiene_nit:
            errores.append("NIT obligatorio para todos los contribuyentes (Decreto 131/2025)")

        declaro_anual = datos.get("declaracion_jurada_presentada", False)
        if not declaro_anual:
            alertas.append("Declaración Jurada anual pendiente (Art. 29 Ley Tributaria)")

        pago_ss = datos.get("pago_seguridad_social_al_dia", False)
        dias_atraso_ss = datos.get("dias_atraso_seguridad_social", 0)
        if not pago_ss:
            if dias_atraso_ss > 10:
                errores.append(f"Seguridad social con {dias_atraso_ss} días de atraso. Plazo: 10 días hábiles del mes (Art. 303)")
            else:
                alertas.append(f"Seguridad social próxima a vencer ({dias_atraso_ss} días de atraso)")

        ventas_mensuales = datos.get("ventas_mensuales_cup", 0)
        pago_ventas = datos.get("impuesto_ventas_pagado", False)
        if ventas_mensuales > 0 and not pago_ventas:
            alertas.append("Impuesto sobre ventas y servicios (10%) pendiente de pago")

        dividendos_distribuidos = datos.get("dividendos_distribuidos_cup", 0)
        retencion_dividendos = datos.get("retencion_dividendos_5pct", False)
        if dividendos_distribuidos > 0 and not retencion_dividendos:
            alertas.append("Retención del 5% sobre distribución anticipada de dividendos pendiente (Art. 26)")

        es_primer_ano = datos.get("es_primer_ano_operaciones", False)
        meses_operando = datos.get("meses_operando", 0)
        if es_primer_ano and meses_operando <= 12:
            return Inferencia(
                tipo="informe",
                descripcion=f"EXENCIÓN VIGENTE: Primer año de operaciones. Exento de tributos excepto seguridad social (mes {meses_operando}/12)",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.VERDE,
                confianza=0.95,
                accion_recomendada="Mantener al día la seguridad social. Preparar para obligaciones tributarias del año 2.",
                plugin_origen=self.nombre
            )

        es_reconversion = datos.get("es_reconversion", False)
        meses_reconversion = datos.get("meses_desde_reconversion", 0)
        if es_reconversion and meses_reconversion <= 6:
            return Inferencia(
                tipo="informe",
                descripcion=f"EXENCIÓN RECONVERSIÓN: {meses_reconversion}/6 meses exentos",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.VERDE,
                confianza=0.95,
                accion_recomendada="Preparar obligaciones tributarias para el mes 7.",
                plugin_origen=self.nombre
            )

        if errores:
            return Inferencia(
                tipo="alerta",
                descripcion=f"OBLIGACIONES TRIBUTARIAS CRÍTICAS: {len(errores)} incumplimientos",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.ROJO,
                confianza=0.95,
                accion_recomendada=f"URGENTE: {'; '.join(errores[:3])}. Riesgo de sanciones y cierre.",
                plugin_origen=self.nombre
            )
        elif alertas:
            return Inferencia(
                tipo="alerta",
                descripcion=f"OBLIGACIONES TRIBUTARIAS PENDIENTES: {len(alertas)} advertencias",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.AMARILLO,
                confianza=0.85,
                accion_recomendada=f"Regularizar: {'; '.join(alertas[:3])}",
                plugin_origen=self.nombre
            )
        else:
            return Inferencia(
                tipo="informe",
                descripcion="TRIBUTACIÓN AL DÍA: Todas las obligaciones cumplidas",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.VERDE,
                confianza=0.95,
                accion_recomendada="Sin acción requerida",
                plugin_origen=self.nombre
            )

    def _procesar_precios(self, datos: Dict, evidencia_id: str) -> Inferencia:
        precio_venta = datos.get("precio_venta", 0)
        precio_costo = datos.get("precio_costo", 0)
        producto_centralizado = datos.get("producto_precio_centralizado", False)
        precio_autorizado = datos.get("precio_autorizado_central", 0)

        if producto_centralizado and precio_venta != precio_autorizado:
            return Inferencia(
                tipo="alerta",
                descripcion=f"PRECIO CENTRALIZADO VIOLADO: Producto con precio autorizado {precio_autorizado} CUP, vendido a {precio_venta} CUP",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.ROJO,
                confianza=1.0,
                accion_recomendada="AJUSTAR PRECIO INMEDIATAMENTE. Riesgo de multa y cierre por violación de precios.",
                plugin_origen=self.nombre
            )

        es_venta_estatal = datos.get("venta_a_sector_estatal", False)
        margen = ((precio_venta - precio_costo) / precio_costo * 100) if precio_costo > 0 else 0.0
        limite_ganancia = datos.get("limite_ganancia_estatal_pct", 0)

        if es_venta_estatal and limite_ganancia > 0 and margen > limite_ganancia:
            return Inferencia(
                tipo="alerta",
                descripcion=f"MARGEN EXCEDIDO EN VENTA AL ESTADO: {margen:.1f}% vs límite {limite_ganancia}%",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.ROJO,
                confianza=0.95,
                accion_recomendada="Revisar precio de venta al sector estatal. Aplicar límite de ganancia establecido.",
                plugin_origen=self.nombre
            )

        margen_muy_alto = datos.get("margen_muy_alto", False)
        if margen_muy_alto:
            return Inferencia(
                tipo="alerta",
                descripcion="POSIBLE PRECIO ABUSIVO: Margen excesivamente alto detectado",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.NARANJA,
                confianza=0.80,
                accion_recomendada="Documentar justificación del precio. Preparar respaldo de costos.",
                plugin_origen=self.nombre
            )

        return Inferencia(
            tipo="informe",
            descripcion=f"Precios dentro de parámetros (margen: {margen:.1f}%)",
            evidencias_usadas=[evidencia_id],
            nivel_alerta=NivelAlerta.VERDE,
            confianza=0.90,
            accion_recomendada="Sin acción requerida",
            plugin_origen=self.nombre
        )

    def _procesar_seguridad_social(self, datos: Dict, evidencia_id: str) -> Inferencia:
        trabajadores_registrados = datos.get("trabajadores_registrados_ss", 0)
        trabajadores_reales = datos.get("trabajadores_reales", 0)
        pago_al_dia = datos.get("pago_seguridad_social_al_dia", True)

        if trabajadores_reales > trabajadores_registrados:
            return Inferencia(
                tipo="alerta",
                descripcion=f"TRABAJADORES NO REGISTRADOS EN SS: {trabajadores_reales - trabajadores_registrados} personas sin afiliación",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.ROJO,
                confianza=0.95,
                accion_recomendada="REGISTRAR TODOS los trabajadores en seguridad social inmediatamente. Multa y sanciones graves.",
                plugin_origen=self.nombre
            )

        if not pago_al_dia:
            return Inferencia(
                tipo="alerta",
                descripcion="PAGO DE SEGURIDAD SOCIAL ATRASADO",
                evidencias_usadas=[evidencia_id],
                nivel_alerta=NivelAlerta.NARANJA,
                confianza=0.90,
                accion_recomendada="Regularizar pago en los primeros 10 días hábiles del mes. Riesgo de sanciones.",
                plugin_origen=self.nombre
   
