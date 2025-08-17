$ErrorActionPreference = "Stop"

# BD temporal para pruebas (evita ensuciar la bd principal)
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$rand = Get-Random -Maximum 100000
$TEST_DB = "demo_db_test_{0}_{1}" -f $timestamp, $rand
Write-Host "→ Running tests in DB: $TEST_DB"

# Asegura que db/odoo estén arriba (idempotente)
docker compose up -d db odoo

# Ejecutar pruebas con aislamiento
docker compose run --rm odoo `
  --db_host=db --db_user=odoo --db_password=odoo `
  -d $TEST_DB `
  -i base,web,sale,odoo_dim_sales `
  --without-demo=all `
  --test-enable `
  --test-tags=/odoo_dim_sales `
  --workers=0 --max-cron-threads=0 `
  --log-level=test `
  --stop-after-init

$code = $LASTEXITCODE
Write-Host "→ Tests exit code: $code"

if ($code -eq 0) {
    Write-Host "`n=============================" -ForegroundColor Green
    Write-Host "✅ All tests passed successfully!" -ForegroundColor Green
    Write-Host "=============================" -ForegroundColor Green
} else {
    Write-Host "`n=============================" -ForegroundColor Red
    Write-Host "❌ Some tests failed (exit code $code)" -ForegroundColor Red
    Write-Host "=============================" -ForegroundColor Red
}

exit $code
