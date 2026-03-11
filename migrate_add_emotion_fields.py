"""
数据库迁移脚本：为 existing emotional_states 和 emotional_history 表添加新字段
运行方式：python migrate_add_emotion_fields.py
"""
import os
from database import get_db, USE_POSTGRES

def migrate():
    """执行数据库迁移"""
    print(f"当前数据库类型：{'PostgreSQL' if USE_POSTGRES else 'SQLite'}")

    # 要添加的新字段
    emotional_states_fields = [
        ("valence", "REAL DEFAULT 0.0"),
        ("arousal", "REAL DEFAULT 0.5"),
        ("behavior_counts", "TEXT"),
        ("extracted_keywords", "TEXT"),
    ]

    emotional_history_fields = [
        ("valence", "REAL DEFAULT 0.0"),
        ("arousal", "REAL DEFAULT 0.5"),
        ("behavior_counts", "TEXT"),
        ("extracted_keywords", "TEXT"),
    ]

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()

            # 检查 emotional_states 表是否已有这些字段
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'emotional_states' AND column_name IN %s
            """, (('valence', 'arousal', 'behavior_counts', 'extracted_keywords'),))
            existing_cols = {row[0] for row in cursor.fetchall()}

            # 添加 emotional_states 新字段
            for field_name, field_type in emotional_states_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to emotional_states...")
                    cursor.execute(f"""
                        ALTER TABLE emotional_states
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in emotional_states")

            # 检查 emotional_history 表是否已有这些字段
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'emotional_history' AND column_name IN %s
            """, (('valence', 'arousal', 'behavior_counts', 'extracted_keywords'),))
            existing_cols = {row[0] for row in cursor.fetchall()}

            # 添加 emotional_history 新字段
            for field_name, field_type in emotional_history_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to emotional_history...")
                    cursor.execute(f"""
                        ALTER TABLE emotional_history
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in emotional_history")

            db.commit()
            cursor.close()

        else:
            # SQLite
            # 检查 emotional_states 表是否已有这些字段
            cursor = db.execute("PRAGMA table_info(emotional_states)")
            existing_cols = {row[1] for row in cursor.fetchall()}

            # 添加 emotional_states 新字段
            for field_name, field_type in emotional_states_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to emotional_states...")
                    db.execute(f"""
                        ALTER TABLE emotional_states
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in emotional_states")

            # 检查 emotional_history 表是否已有这些字段
            cursor = db.execute("PRAGMA table_info(emotional_history)")
            existing_cols = {row[1] for row in cursor.fetchall()}

            # 添加 emotional_history 新字段
            for field_name, field_type in emotional_history_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to emotional_history...")
                    db.execute(f"""
                        ALTER TABLE emotional_history
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in emotional_history")

            db.commit()

    print("迁移完成！")


if __name__ == "__main__":
    migrate()
