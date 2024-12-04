CREATE DATABASE IF NOT EXISTS marketug_db;
USE marketug_db;

CREATE TABLE IF NOT EXISTS  usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    carrera VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS  productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad INT DEFAULT 1,
    id_usuario INT,
    categoria VARCHAR(100),
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('disponible', 'vendido') DEFAULT 'disponible',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS  pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'completado', 'cancelado') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS detalles_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    id_producto INT,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS mensajes (
    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
    id_emisor INT NOT NULL,
    id_receptor INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_emisor) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_receptor) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_comprador INT NOT NULL,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_comprador) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);


INSERT INTO usuarios (nombre, correo, contrasena, carrera) VALUES
('Juan Pérez', 'j.perez@ugto.mx', 'password1', 'Ingeniería'),
('Ana López', 'a.lopez@ugto.mx', 'password2', 'Medicina'),
('Luis García', 'l.garcia@ugto.mx', 'password3', 'Derecho');

INSERT INTO productos (nombre, descripcion, precio, cantidad, id_usuario, categoria) VALUES
('Libro de Física', 'Libro de texto de física para principiantes', 250.00, 3, 1, 'Libros'),
('Calculadora Científica', 'Calculadora Casio FX-991', 150.00, 5, 1, 'Tecnología'),
('Estetoscopio', 'Estetoscopio de alta calidad para estudiantes de medicina', 300.00, 2, 2, 'Salud'),
('Código Civil', 'Código Civil actualizado 2024', 100.00, 4, 3, 'Libros');

INSERT INTO pedidos (id_usuario, estado) VALUES
(3, 'pendiente');

INSERT INTO detalles_pedido (id_pedido, id_producto, cantidad, precio) VALUES
(1, 1, 1, 250.00),  -- Compra de 1 unidad del "Libro de Física"
(1, 2, 1, 150.00);  -- Compra de 1 unidad de la "Calculadora Científica"

SELECT * FROM usuarios;
SELECT * FROM productos WHERE estado = 'disponible';
ALTER TABLE productos MODIFY id_usuario INT NOT NULL;
ALTER TABLE productos ADD CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;
ALTER TABLE productos ADD CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL;


INSERT INTO categorias (nombre_categoria) VALUES
('Tecnología'),
('Hogar'),
('Deportes'),
("Libros"),
('Moda');