CREATE TABLE clientes (
    id UUID PRIMARY KEY,
    nombre TEXT NOT NULL,
    sexo TEXT CHECK (sexo IN ('M','F')),
    fecha_nacimiento DATE,
    creado_en TIMESTAMP DEFAULT now()
);

INSERT INTO clientes (id, nombre, sexo, fecha_nacimiento) VALUES
('3d72af43-cac4-4ad1-aa48-4139d06d7963','Juan Pérez','M','1990-05-15'),
('b2c0ca75-2f49-43b2-a588-695abc3c38fe','María Gómez','F','1985-10-20'),
('9784d0e0-4106-451f-bd05-f7c0fb650c18','Carlos Sánchez','M','2000-01-10'),
('7aac5ea1-80c5-4d1c-a1c1-948cf6954f34','Ana Rodríguez','F','1995-07-30'),
('f9f1b76f-74f6-47e2-8366-bb8d99c6afd4','Luis Fernández','M','1988-12-05'),
('c9c776e5-6d48-42fa-b63a-163c3faa1483','Sofía Martínez','F','2002-03-14'),
('f3d6f0ad-5565-41ef-a0e7-d9acc204f659','Pedro López','M','1992-06-18'),
('0c29e21a-8e83-4d22-8f0e-f36ff8088221','Laura Torres','F','1987-09-09'),
('16aa619b-b698-4ac4-b8d8-b68af6f365fe','Miguel Ramírez','M','1998-11-25'),
('024f4324-d0c6-405b-812e-f40c6822da82','Clara Jiménez','F','1993-04-04');

CREATE TABLE productos (
    id UUID PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);

INSERT INTO productos (id, nombre, precio) VALUES
('cee8d30a-bd61-4e59-9879-b472c7ffbec9','Laptop',1500.00),
('c35f50eb-18e5-4654-a35d-834c30809454','Smartphone',800.00),
('52d054a8-27ef-4e41-b473-2528095c3a11','Tablet',400.00),
('659978b7-304a-42f0-95fe-25ac6787d885','Monitor',250.00),
('f0a43028-2c14-4d17-ab15-aedd3d96b23b','Teclado',50.00);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    cliente_id UUID NOT NULL REFERENCES clientes(id),
    producto_id UUID NOT NULL REFERENCES productos(id),
    cantidad INT NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    fecha TIMESTAMP NOT NULL
);

INSERT INTO ventas (cliente_id, producto_id, cantidad, total, fecha) VALUES
('3d72af43-cac4-4ad1-aa48-4139d06d7963','cee8d30a-bd61-4e59-9879-b472c7ffbec9',1,1500.00,'2025-01-05'),
('3d72af43-cac4-4ad1-aa48-4139d06d7963','c35f50eb-18e5-4654-a35d-834c30809454',2,1600.00,'2025-01-15'),
('b2c0ca75-2f49-43b2-a588-695abc3c38fe','52d054a8-27ef-4e41-b473-2528095c3a11',1,400.00,'2025-02-10'),
('9784d0e0-4106-451f-bd05-f7c0fb650c18','659978b7-304a-42f0-95fe-25ac6787d885',3,750.00,'2025-01-20'),
('7aac5ea1-80c5-4d1c-a1c1-948cf6954f34','f0a43028-2c14-4d17-ab15-aedd3d96b23b',5,250.00,'2025-03-01');