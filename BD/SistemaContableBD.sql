create table plan_cuentas (
    id_cuenta bigint generated always as identity primary key,
    codigo varchar(20) not null unique,
    nombre varchar(100) not null,

    tipo text not null check (
        tipo in ('ACTIVO','PASIVO','PATRIMONIO','INGRESO','COSTO','GASTO')
    ),

    naturaleza text not null check (
        naturaleza in ('DEUDORA','ACREEDORA')
    ),

    nivel int not null,

    id_padre bigint null,

    estado boolean default true,

    constraint fk_plan_cuentas
        foreign key (id_padre)
        references plan_cuentas (id_cuenta)
);

