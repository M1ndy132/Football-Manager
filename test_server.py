import sys
sys.path.insert(0, '.')

print('Testing imports after cleaning null bytes...')

# Test config import
try:
    from app.core.config import settings
    print('✅ Config import successful')
    print(f'Database URL: {settings.DATABASE_URL}')
except Exception as e:
    print(f'❌ Config import failed: {e}')
    import traceback
    traceback.print_exc()

# Test session import
try:
    from app.database.session import get_db
    print('✅ Session import successful')
except Exception as e:
    print(f'❌ Session import failed: {e}')

# Test schemas import
try:
    from app.schemas.team import TeamCreate
    print('✅ Schemas import successful')
except Exception as e:
    print(f'❌ Schemas import failed: {e}')

# Test router import
try:
    from app.routers.team_router import router
    print('✅ Team router import successful')
except Exception as e:
    print(f'❌ Team router import failed: {e}')
print(f'❌ Team router import failed: {e}')