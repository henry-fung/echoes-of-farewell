"""
数据库迁移脚本：为 chat_messages 表添加失败状态和重试相关字段
运行方式：python migrate_add_message_retry_fields.py
"""
import os
from database import get_db, USE_POSTGRES

def migrate():
    """执行数据库迁移"""
    print(f"当前数据库类型：{'PostgreSQL' if USE_POSTGRES else 'SQLite'}")

    # 要添加的新字段
    new_fields = [
        ("is_failed", "BOOLEAN DEFAULT FALSE"),  # 标记消息是否失败
        ("error_message", "TEXT"),  # 存储错误信息
        ("parent_id", "INTEGER"),  # 如果是重试消息，指向原始消息 ID
    ]

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()

            # 检查 chat_messages 表是否已有这些字段
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'chat_messages' AND column_name IN %s
            """, (('is_failed', 'error_message', 'parent_id'),))
            existing_cols = {row[0] for row in cursor.fetchall()}

            # 添加新字段
            for field_name, field_type in new_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to chat_messages...")
                    cursor.execute(f"""
                        ALTER TABLE chat_messages
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in chat_messages")

            db.commit()
            cursor.close()

        else:
            # SQLite
            cursor = db.execute("PRAGMA table_info(chat_messages)")
            existing_cols = {row[1] for row in cursor.fetchall()}

            # 添加新字段
            for field_name, field_type in new_fields:
                if field_name not in existing_cols:
                    print(f"Adding {field_name} to chat_messages...")
                    db.execute(f"""
                        ALTER TABLE chat_messages
                        ADD COLUMN {field_name} {field_type}
                    """)
                else:
                    print(f"Field {field_name} already exists in chat_messages")

            db.commit()

    print("迁移完成！")


if __name__ == "__main__":
    migrate()
