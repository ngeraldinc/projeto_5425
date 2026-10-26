CREATE TABLE IF NOT EXISTS "cliente" (
	"id_cliente" SERIAL NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"telefone" VARCHAR(30) NOT NULL UNIQUE,
	"email" VARCHAR(50) NOT NULL,
	PRIMARY KEY("id_cliente")
);

CREATE TABLE IF NOT EXISTS "administrador" (
	"id_admin" SERIAL NOT NULL,
	"nome" VARCHAR(100) NOT NULL,
	"email" VARCHAR(50) NOT NULL UNIQUE,
	"palavra_passe" VARCHAR(50) NOT NULL,
	PRIMARY KEY("id_admin")
);

CREATE TABLE IF NOT EXISTS "servico" (
	"id_servico" SERIAL NOT NULL,
	"nome" VARCHAR(50) NOT NULL,
	"descricao" VARCHAR(100) NOT NULL,
	"preco" DECIMAL(10,2) NOT NULL,
	PRIMARY KEY("id_servico")
);

CREATE TABLE IF NOT EXISTS "marcacao" (
	"id_marcacao" SERIAL NOT NULL,
	"data" DATE NOT NULL,
	"hora" TIME NOT NULL,
	"estado" VARCHAR(20) NOT NULL CHECK(estado IN ('realizada', 'cancelada', 'falta')),
	"id_cliente" INTEGER NOT NULL,
	PRIMARY KEY("id_marcacao")
);

CREATE TABLE IF NOT EXISTS "marcacao_servico" (
	"id_marcacao" INTEGER NOT NULL,
	"id_servico" INTEGER NOT NULL,
	PRIMARY KEY("id_marcacao", "id_servico")
);

ALTER TABLE "marcacao"
ADD FOREIGN KEY("id_cliente") REFERENCES "cliente"("id_cliente")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "marcacao_servico"
ADD FOREIGN KEY("id_servico") REFERENCES "servico"("id_servico")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "marcacao_servico"
ADD FOREIGN KEY("id_marcacao") REFERENCES "marcacao"("id_marcacao")
ON UPDATE NO ACTION ON DELETE NO ACTION;

CREATE UNIQUE INDEX IF NOT EXISTS uq_marcacao_data_hora_ativa
ON "marcacao" ("data", "hora")
WHERE "estado" <> 'cancelada';