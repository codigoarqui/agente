from langchain_core.tools import tool
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GEMINI_API_KEY
from app.core.sql_database import db

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

table_info = {
    "clientes": ["id", "nombre", "sexo", "edad", "fecha_nacimiento"],
    "productos": ["id", "nombre", "precio", "descuento", "stock"],
    "ventas": ["id", "cliente_id", "producto_id", "cantidad", "total", "fecha"]
}

few_shot_examples = [
    {
        "pregunta": "Qué productos tengo registrados?",
        "sql": "SELECT nombre FROM productos;"
    },
    {
        "pregunta": "Quién es el cliente más joven?",
        "sql": "SELECT nombre, fecha_nacimiento FROM clientes ORDER BY fecha_nacimiento DESC LIMIT 1;"
    },
    {
        "pregunta": "Quién ha comprado más?",
        "sql": "SELECT c.nombre, SUM(v.cantidad) AS total_vendido FROM ventas v JOIN clientes c ON v.cliente_id = c.id GROUP BY c.nombre ORDER BY total_vendido DESC LIMIT 1;"
    },
    {
        "pregunta": "Cuál es el producto más vendido en enero?",
        "sql": "SELECT p.nombre, SUM(v.cantidad) AS total_vendido FROM ventas v JOIN productos p ON v.producto_id = p.id WHERE EXTRACT(MONTH FROM v.fecha) = 1 GROUP BY p.nombre ORDER BY total_vendido DESC LIMIT 1;"
    }
]

@tool
def consultar_base_de_datos_clientes(consulta_en_lenguaje_natural: str) -> str:
    """
    Esta herramienta permite responder consultas sobre clientes, productos y ventas.
    El usuario puede preguntar cualquier cosa en lenguaje natural, por ejemplo:
    - 'Cuántos clientes tengo registrados'
    - 'Quién es el cliente más joven'
    - 'Qué productos puedo comprar'
    - 'Qué productos están en descuento'
    - 'Quién vendió más en enero'

    Columnas disponibles y relaciones:
    - Clientes: 'id', 'nombre', 'sexo', 'edad', 'fecha_nacimiento'
    - Productos: 'id', 'nombre', 'precio', 'descuento', 'stock'
    - Ventas: 'id', 'cliente_id', 'producto_id', 'cantidad', 'total', 'fecha'

    El agente se encarga de traducir estas preguntas a SQL automáticamente y devolver los resultados.
    """
    
    print(f"--- Herramienta SQL recibiendo consulta: {consulta_en_lenguaje_natural} ---")
    
    try:
        sql_agent_executor = create_sql_agent(
            llm,
            db=db,
            agent_type="tool-calling",
            verbose=True,
            table_info=table_info,
            few_shot_examples=few_shot_examples
        )
        
        response = sql_agent_executor.invoke({"input": consulta_en_lenguaje_natural})
        
        if hasattr(response, "intermediate_steps"):
            for step in response.intermediate_steps:
                if "sql" in step:
                    print(f"SQL generada: {step['sql']}")
        
        return response.get("output", "No se pudo obtener una respuesta de la base de datos.")
    
    except Exception as e:
        return f"Error al consultar la base de datos con SQL: {e}"