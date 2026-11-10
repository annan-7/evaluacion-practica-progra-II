## Evualuacion Progra II

 uv run src/evaluacion_practica_progra_ii/main.py

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 1
Título: Python 
Autor: xyz
Ejemplares disponibles: 5
Libro(id=1, titulo='Python', autor='xyz', disponibles=5)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 1
Título: Base de datos
Autor: xuy
Ejemplares disponibles: 3
Libro(id=2, titulo='Base de datos', autor='xuy', disponibles=3)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 2
Libro(id=1, titulo='Python', autor='xyz', disponibles=5)
Libro(id=2, titulo='Base de datos', autor='xuy', disponibles=3)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 6
Nombre: mati
Correo: mato@gmail.com
Usuario(id=1, nombre='mati', correo='mato@gmail.com')

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 11
ID libro: 1
ID usuario: 1 
Cantidad: 2
Fecha AAAA-MM-DD (Enter = hoy): 23-09-2020
Fecha inválida. Ejemplo: 2026-11-10
Fecha AAAA-MM-DD (Enter = hoy): 
Préstamo registrado: Prestamo(id=1, libro_id=1, usuario_id=1, cantidad=2, fecha=2026-11-10, estado=Activo)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 2
Libro(id=1, titulo='Python', autor='xyz', disponibles=3)
Libro(id=2, titulo='Base de datos', autor='xuy', disponibles=3)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 14
ID préstamo: 1
Devuelto: Prestamo(id=1, libro_id=1, usuario_id=1, cantidad=2, fecha=2026-11-10, estado=Devuelto)

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 14
ID préstamo: 1
Error: Este préstamo ya fue devuelto

=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir
Opción: 0
Hasta luego.
