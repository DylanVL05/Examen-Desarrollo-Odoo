#!/usr/bin/env bash
set -euo pipefail

# BD temporal para pruebas (no ensucia tu demo_db)
TEST_DB="demo_db_test_$(date +%Y%m%d_%H%M%S)_$RANDOM"
echo "→ Running tests in DB: $TEST_DB"

# Asegura que db/odoo estén arriba (idempotente)
docker compose up -d db odoo

# Ejecuta pruebas con aislamiento
docker compose run --rm odoo \
  --db_host=db --db_user=odoo --db_password=odoo \
  -d "$TEST_DB" \
  -i base,web,sale,odoo_dim_sales \
  --without-demo=all \
  --test-enable \
  --test-tags=/odoo_dim_sales \
  --workers=0 --max-cron-threads=0 \
  --log-level=test \
  --stop-after-init

EXIT=$?

#  Resultado llamativo en consola
if [ $EXIT -eq 0 ]; then
  echo -e "\n\033[1;32m🎉 PRUEBAS EXITOSAS: 0 failed, 0 errors ✅\033[0m\n"
else
  echo -e "\n\033[1;31m❌ PRUEBAS FALLIDAS: revisa los logs ❌\033[0m\n"
fi

echo "→ Tests exit code: $EXIT"
exit $EXIT
