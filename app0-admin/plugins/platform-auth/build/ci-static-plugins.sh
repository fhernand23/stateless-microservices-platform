echo "==========================="
echo "CI STATIC ANALYSIS: PLUGINS"
echo "==========================="
code=0

echo "platform-auth"
export MYPYPATH=app0-admin/src/:plugins/platform-auth/src/ && python3 -m mypy --namespace-packages -p app0.platform.auth
code+=$?
export MYPYPATH=app0-admin/src/:plugins/platform-auth/src/ && python3 -m mypy --namespace-packages plugins/platform-auth/test/unit/
code+=$?
python3 -m flake8 --max-line-length=120 plugins/platform-auth/src/app0/ plugins/platform-auth/test/unit/ 
code+=$?
python3 -m pylint plugins/platform-auth/src/app0/platform/auth
code+=$?

if [ $code -gt 0 ]
then
  echo "[FAILED] CI STATIC ANALYSIS: PLUGINS"
fi
echo "========================================================================================================"
exit $code
