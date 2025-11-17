"""
Init migration
"""

from yoyo import step

__depends__ = {}

steps = """
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
        "email" VARCHAR(100) NOT NULL UNIQUE,
        "password" VARCHAR(255) NOT NULL,
        "test_id" UUID,
        "created_at" TIMESTAMP NOT NULL DEFAULT now()
    );

    CREATE TABLE "StreakUpd" (
        "id" UUID NOT NULL PRIMARY KEY,
        "count" INT NOT NULL DEFAULT 0,
        "last_update" timestamp NOT NULL,
        "user_id" UUID NOT NULL
    );

    CREATE TABLE "Session" (
        "id" UUID NOT NULL PRIMARY KEY,
        "user_id" UUID NOT NULL,
        "session_token" VARCHAR NOT NULL,
        "created_at" TIMESTAMP NOT NULL,
        "expire_in" TIMESTAMP NOT NULL
    );

    CREATE TABLE "Calendar" (
        "id" UUID NOT NULL PRIMARY KEY,
        "date" TIMESTAMP NOT NULL,
        "mood_type_id" UUID,
        "user_id" UUID NOT NULL
    );
    
    CREATE TABLE "ToDoCalendar" (
        "id" UUID NOT NULL PRIMARY KEY,
        "date" TIMESTAMP NOT NULL,
        "user_id" UUID NOT NULL
    );

    CREATE TABLE "ToDoMood" (
        "id" UUID NOT NULL PRIMARY KEY,
        "advice" VARCHAR(1000),
        "checkbox" BOOLEAN NOT NULL DEFAULT false,
        "time_start" VARCHAR(100),
        "time_end" VARCHAR(100),
        "todo_calendar_id" UUID NOT NULL,
        "mood_type_id" UUID NOT NULL
    );

    CREATE TABLE "OnboardingTestResult" (
        "id" UUID NOT NULL PRIMARY KEY,
        "result" JSONB NOT NULL,
        "personality_type" personality_type,
        "user_id" UUID
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

    -- Foreign key constraints
    ALTER TABLE "StreakUpd"
    ADD FOREIGN KEY ("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "Session"
    ADD FOREIGN KEY ("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "ToDoCalendar"
    ADD FOREIGN KEY ("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "ToDoMood"
    ADD FOREIGN KEY ("todo_calendar_id") REFERENCES "ToDoCalendar"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "ToDoMood"
    ADD FOREIGN KEY ("mood_type_id") REFERENCES "MoodType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Calendar"
    ADD FOREIGN KEY ("mood_type_id") REFERENCES "MoodType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Calendar"
    ADD FOREIGN KEY ("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "OnboardingTestResult"
    ADD FOREIGN KEY ("user_id") REFERENCES "User"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY ("mood_type_id") REFERENCES "MoodType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY ("activity_type_id") REFERENCES "ActivityType"("id")
    ON UPDATE NO ACTION ON DELETE NO ACTION;
    
    ALTER TABLE "Mood"
    ADD FOREIGN KEY ("calendar_id") REFERENCES "Calendar"("id")
    ON UPDATE NO ACTION ON DELETE CASCADE;

    -- Indexes
    CREATE INDEX idx_session_user_id ON "Session" ("user_id");
    CREATE INDEX idx_session_token ON "Session" ("session_token");
    CREATE INDEX idx_calendar_user_date ON "Calendar" ("user_id", "date");
    CREATE INDEX idx_calendar_date ON "Calendar" ("date");
    CREATE INDEX idx_mood_calendar_id ON "Mood" ("calendar_id");
    CREATE INDEX idx_todo_calendar_user_id ON "ToDoCalendar" ("user_id");
    CREATE INDEX idx_todo_calendar_date ON "ToDoCalendar" ("date");
    CREATE INDEX idx_todo_mood_calendar_id ON "ToDoMood" ("todo_calendar_id");
    CREATE INDEX idx_user_email ON "User" ("email");
    CREATE INDEX idx_test_result_user_id ON "OnboardingTestResult" ("user_id");

    -- Insert initial data
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
    DROP TABLE IF EXISTS "ToDoMood" CASCADE;
    DROP TABLE IF EXISTS "ToDoCalendar" CASCADE;
    DROP TABLE IF EXISTS "Mood" CASCADE;
    DROP TABLE IF EXISTS "StreakUpd" CASCADE;
    DROP TABLE IF EXISTS "OnboardingTestResult" CASCADE;
    DROP TABLE IF EXISTS "Calendar" CASCADE;
    DROP TABLE IF EXISTS "Session" CASCADE;
    DROP TABLE IF EXISTS "User" CASCADE;
    DROP TABLE IF EXISTS "MoodType" CASCADE;
    DROP TABLE IF EXISTS "ActivityType" CASCADE;
    DROP TYPE IF EXISTS personality_type CASCADE;
    """)
]