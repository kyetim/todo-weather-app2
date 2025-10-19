-- Sadece yeni tabloları ekle (mevcut tabloları etkilemez)

-- Kategoriler tablosu (OOP ilişkiler için)
CREATE TABLE IF NOT EXISTS categories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff', -- Hex renk kodu
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todo'lar tablosunu güncelle (yeni sütunlar ekle)
ALTER TABLE todos ADD COLUMN IF NOT EXISTS category_id UUID REFERENCES categories(id) ON DELETE SET NULL;
ALTER TABLE todos ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE todos ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));
ALTER TABLE todos ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE todos ADD COLUMN IF NOT EXISTS tags TEXT[];

-- Todo-kategori ilişkisi (Many-to-Many)
CREATE TABLE IF NOT EXISTS todo_categories (
    todo_id UUID REFERENCES todos(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (todo_id, category_id)
);

-- Hava durumu geçmişi (API kullanımı için)
CREATE TABLE IF NOT EXISTS weather_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    city VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2),
    description VARCHAR(100),
    humidity INTEGER,
    icon VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- İndeksler (performans için)
CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
CREATE INDEX IF NOT EXISTS idx_todos_due_date ON todos(due_date);
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);
CREATE INDEX IF NOT EXISTS idx_weather_user_city ON weather_history(user_id, city);

-- Updated_at otomatik güncelleme trigger'ı
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger'ları ekle (eğer yoksa)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_users_updated_at') THEN
        CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_todos_updated_at') THEN
        CREATE TRIGGER update_todos_updated_at BEFORE UPDATE ON todos
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;
