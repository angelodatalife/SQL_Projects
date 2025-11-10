import sqlite3
from tabulate import tabulate # Necesitarás 'pip install tabulate'

# Nombre del archivo de la base de datos SQLite (debe existir)
DB_FILE = "sakila.db"

# --- CONSULTAS SQL (Las mismas que generamos antes para SQLite) ---
# ... (usa el diccionario QUERIES definido en la respuesta anterior)

QUERIES = {
    1: {
        "title": "1. Tienda, Ciudad y País",
        "sql": """
            SELECT s.store_id AS "ID de Tienda", c.city AS Ciudad, cy.country AS País
            FROM store s
            JOIN address a ON s.address_id = a.address_id
            JOIN city c ON a.city_id = c.city_id
            JOIN country cy ON c.country_id = cy.country_id;
        """
    },
    2: {
        "title": "2. Ingresos Totales por Tienda",
        "sql": """
            SELECT s.store_id AS "ID de Tienda", SUM(p.amount) AS "Ingreso Total ($)"
            FROM payment p
            JOIN staff st ON p.staff_id = st.staff_id
            JOIN store s ON st.store_id = s.store_id
            GROUP BY s.store_id
            ORDER BY "Ingreso Total ($)" DESC;
        """
    },
    3: {
        "title": "3. Duración Promedio de Películas por Categoría",
        "sql": """
            SELECT c.name AS "Categoría", AVG(f.length) AS "Duración Promedio (min)"
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            GROUP BY c.name
            ORDER BY "Duración Promedio (min)" DESC;
        """
    },
    4: {
        "title": "4. Categorías de Películas Más Largas",
        "sql": """
            SELECT c.name AS "Categoría", AVG(f.length) AS "Duración Promedio (min)"
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            GROUP BY c.name
            ORDER BY "Duración Promedio (min)" DESC;
        """
    },
    5: {
        "title": "5. Películas Más Alquiladas (Descendente)",
        "sql": """
            SELECT f.title AS "Título de la Película", COUNT(r.rental_id) AS "Total de Alquileres"
            FROM film f
            JOIN inventory i ON f.film_id = i.film_id
            JOIN rental r ON i.inventory_id = r.inventory_id
            GROUP BY f.title
            ORDER BY "Total de Alquileres" DESC;
        """
    },
    6: {
        "title": "6. Top 5 Géneros por Ingresos Brutos",
        "sql": """
            SELECT c.name AS Género, SUM(p.amount) AS "Ingresos Brutos"
            FROM category c
            JOIN film_category fc ON c.category_id = fc.category_id
            JOIN inventory i ON fc.film_id = i.film_id
            JOIN rental r ON i.inventory_id = r.inventory_id
            JOIN payment p ON r.rental_id = p.rental_id
            GROUP BY c.name
            ORDER BY "Ingresos Brutos" DESC
            LIMIT 5;
        """
    },
    7: {
        "title": '7. ¿"Academy Dinosaur" disponible para alquilar en la Tienda 1?',
        "sql": """
            SELECT COUNT(i.inventory_id) AS "Copias Disponibles"
            FROM film f
            JOIN inventory i ON f.film_id = i.film_id
            LEFT JOIN rental r ON i.inventory_id = r.inventory_id AND r.return_date IS NULL
            WHERE f.title = 'ACADEMY DINOSAUR'
            AND i.store_id = 1
            AND r.rental_id IS NULL;
        """
    }
}


def execute_sqlite_query_and_display(query_data):
    """Conecta a la DB SQLite, ejecuta una consulta y muestra los resultados."""
    print(f"\n{'='*70}\n{query_data['title']}\n{'='*70}")
    
    conn = None
    try:
        # 1. Establecer conexión con el archivo DB
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # 2. Ejecutar la consulta
        cursor.execute(query_data["sql"])
        
        # 3. Obtener resultados y encabezados
        results = cursor.fetchall()
        # Obtener los nombres de las columnas (necesario para tabulate)
        columns = [description[0] for description in cursor.description]

        # 4. Mostrar resultados de forma legible
        if results:
            # Reemplazar el nombre de columna en el encabezado para el Ejercicio 7
            if query_data['title'].startswith('7'):
                print(f"Resultado de disponibilidad: {results[0][0]}")
            else:
                print(tabulate(results, headers=columns, tablefmt="fancy_grid"))
        else:
            print("No se encontraron resultados para esta consulta.")
            
        cursor.close()

    except sqlite3.Error as err:
        print(f"Error de base de datos SQLite: {err}")
        print("Asegúrate de que el archivo 'sakila.db' exista y contenga el esquema de Sakila.")
    except ImportError:
        print("\n*** ERROR: Falta la biblioteca 'tabulate'. Instálala con: pip install tabulate ***")
    finally:
        # 5. Cerrar conexión
        if conn:
            conn.close()

# --- Bucle principal para ejecutar todos los ejercicios ---
if __name__ == "__main__":
    # La clave 4 es idéntica a la 3, pero la incluimos para seguir la numeración
    for index in sorted(QUERIES.keys()):
        execute_sqlite_query_and_display(QUERIES[index])