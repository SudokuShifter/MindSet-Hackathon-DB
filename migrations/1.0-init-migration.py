"""
Init migration
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
    """
    CREATE TYPE personality_type as ENUM ('Сангвиник', 'Холерик', 'Меланхолик', 'Флегматик');

    CREATE TABLE "User" (
        "id" UUID NOT NULL PRIMARY KEY,
        "first_name" VARCHAR(100) NOT NULL,
        "second_name" VARCHAR(100) NOT NULL,
        "email" VARCHAR(100),
        "password" VARCHAR(255),
        "description" VARCHAR(1000),
        "personality_type" personality_type,
        "created_at" TIMESTAMP NOT NULL
    );

    CREATE TABLE "Session" (
        "id" UUID NOT NULL PRIMARY KEY,
        "user_id" UUID NOT NULL,
        "created_at" TIMESTAMP NOT NULL,
        "expire_in" TIMESTAMP NOT NULL
    );

    CREATE TABLE "Calendar" (
        "id" UUID NOT NULL PRIMARY KEY,
        "date" TIMESTAMP NOT NULL,
        "mood_type_id" UUID NOT NULL,
        "user_id" UUID NOT NULL,
        "advice_id" UUID
    );

    CREATE TABLE "LLMAdvice" (
        "id" UUID NOT NULL PRIMARY KEY,
        "advice" VARCHAR(1000) NOT NULL,
        "checkbox" BOOLEAN NOT NULL DEFAULT 'false',
        "created_at" TIMESTAMP
    );

    CREATE TABLE "Mood" (
        "id" UUID NOT NULL PRIMARY KEY,
        "mood_type_id" UUID NOT NULL,
        "activity_type_id" UUID NOT NULL,
        "time_start" VARCHAR(100),
        "time_end" VARCHAR(100),
        "calendar_id" UUID NOT NULL
    );

    CREATE TABLE "MoodType" (
        "id" UUID NOT NULL PRIMARY KEY,
        "title" VARCHAR(100),
        "description" TEXT,
        "score" INT NOT NULL DEFAULT 0
    );

    CREATE TABLE "ActivityType" (
        "id" UUID NOT NULL PRIMARY KEY,
        "title" VARCHAR(100),
        "description" TEXT
    );

    ALTER TABLE "Session"
    ADD FOREIGN KEY("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "Calendar"
    ADD FOREIGN KEY("mood_type_id") REFERENCES "MoodType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Calendar"
    ADD FOREIGN KEY("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "Calendar"
    ADD FOREIGN KEY("advice_id") REFERENCES "LLMAdvice"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY("mood_type_id") REFERENCES "MoodType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY("activity_type_id") REFERENCES "ActivityType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY("calendar_id") REFERENCES "Calendar"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;

    CREATE INDEX ON "Session" ("user_id");
    CREATE INDEX ON "Calendar" ("user_id", "date");
    CREATE INDEX ON "Mood" ("calendar_id");

    INSERT INTO "MoodType" (id, title, description, score) VALUES 
    (gen_random_uuid(), 'Спокойствие', 'Состояние умиротворения и отсутствия тревоги', 8),
    (gen_random_uuid(), 'Волнение', 'Чувство трепета и предвкушения', 7),
    (gen_random_uuid(), 'Счастье', 'Состояние радости и удовлетворения', 10),
    (gen_random_uuid(), 'Смущение', 'Чувство неловкости и стеснения', 3),
    (gen_random_uuid(), 'Грусть', 'Состояние печали и тоски', 2),
    (gen_random_uuid(), 'Злость', 'Чувство раздражения и гнева', 1),
    (gen_random_uuid(), 'Расслабленность', 'Состояние покоя и отсутствия напряжения', 7),
    (gen_random_uuid(), 'Восторг', 'Сильная радость и восхищение', 9),
    (gen_random_uuid(), 'Скука', 'Состояние отсутствия интереса и занятий', 4),
    (gen_random_uuid(), 'Замешательство', 'Чувство растерянности и непонимания', 3),
    (gen_random_uuid(), 'Дискомфорт', 'Общее чувство неудобства и неприятных ощущений', 2),
    (gen_random_uuid(), 'Неудобство', 'Чувство физического или психологического неудобства', 2);

    INSERT INTO "ActivityType" (id, title, description) VALUES 
    (gen_random_uuid(), 'Сон', 'Время для отдыха и восстановления организма'),
    (gen_random_uuid(), 'Тренировка', 'Физические упражнения для поддержания формы'),
    (gen_random_uuid(), 'Домашние дела', 'Повседневные домашние обязанности и уборка'),
    (gen_random_uuid(), 'Кофе-брейк', 'Перерыв для кофе или другого напитка'),
    (gen_random_uuid(), 'Работа', 'Профессиональная деятельность и рабочие задачи'),
    (gen_random_uuid(), 'Приём пищи', 'Время для еды и питания'),
    (gen_random_uuid(), 'Общение', 'Социальное взаимодействие с другими людьми'),
    (gen_random_uuid(), 'Чтение', 'Чтение книг, статей или других материалов'),
    (gen_random_uuid(), 'Учёба', 'Образовательная деятельность и обучение'),
    (gen_random_uuid(), 'Отдых', 'Свободное время для расслабления и хобби');
    """,
    """
    DROP TYPE IF EXISTS public.personality_type CASCADE;
    DROP TABLE IF EXISTS "User";
    DROP TABLE IF EXISTS "Session";
    DROP TABLE IF EXISTS "Calendar";
    DROP TABLE IF EXISTS "LLMAdvice";
    DROP TABLE IF EXISTS "Mood";
    DROP TABLE IF EXISTS "MoodType";
    DROP TABLE IF EXISTS "ActivityType";
    """)
]
