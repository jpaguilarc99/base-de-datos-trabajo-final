INSERT INTO Autor (id_autor, nombre_autor, iniciales_autor, pais_autor) VALUES
(1, 'Gabriel García Márquez', 'GGM', 'Colombia'),
(2, 'Julio Cortázar', 'JC', 'Argentina');

INSERT INTO Editorial (id_editorial, nombre_editorial, pais_editorial, tipo_editorial) VALUES
(1, 'Editorial Planeta', 'España', 'Grande'),
(2, 'Siglo XXI Editores', 'México', 'Mediana');

INSERT INTO Programa (id_programa, nombre_programa) VALUES
(1, 'Ingeniería de Sistemas'),
(2, 'Medicina');

INSERT INTO Material (id_material, id_autor, id_editorial, año_publicacion, tipo, dias_prestamo, ISBN) VALUES
(1, 1, 1, 2020, 'Libro', 30, '978-3-16-148410-0'),
(2, 2, 2, 2018, 'Revista', 15, '978-3-16-148411-7');

INSERT INTO Estudiante (id_estudiante, id_programa, nombre_estudiante, apellido_estudiante, email, telefono) VALUES
(1, 1, 'Juan', 'Pérez', 'juan.perez@example.com', '1234567890'),
(2, 2, 'Ana', 'López', 'ana.lopez@example.com', '0987654321');

INSERT INTO Prestamo (id_prestamo, id_material, id_estudiante, fecha_inicio, fecha_final, dias_prestamo, valor_mora, perdido) VALUES
(1, 1, 1, '2024-05-01', '2024-05-31', 30, 50.00, 0),
(2, 2, 2, '2024-04-01', '2024-04-16', 15, 0.00, 1);

INSERT INTO MaterialXAutor (id_material, id_autor) VALUES
(1, 1),
(2, 2);

INSERT INTO EditorialXMaterial (id_editorial, id_material) VALUES
(1, 1),
(2, 2);

INSERT INTO Area (id_area, nombre_area, descripcion_area, id_material) VALUES
(1, 'Literatura', 'Obras literarias destacadas', 1),
(2, 'Ciencia', 'Publicaciones científicas', 2);