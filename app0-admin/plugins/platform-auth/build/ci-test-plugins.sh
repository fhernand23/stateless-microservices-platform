echo "================"
echo "CI TEST: PLUGINS"
echo "================"
code=0

# auth/platform-auth
export PYTHONPATH=plugins/platform-auth/src/ ELASTICSEARCH_URL=https://localhost:9200 && python3 -m pytest -v --cov-fail-under=90 --cov-report=term --cov=plugins/platform-auth/src/ plugins/platform-auth/test/unit/
code+=$?

if [ $code -gt 0 ]
then
  echo "[FAILED] CI TEST: PLUGINS"
  exit 1
fi
echo "========================================================================================================"
exit $code
