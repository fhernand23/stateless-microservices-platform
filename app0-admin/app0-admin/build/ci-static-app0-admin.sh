echo "==============================="
echo "CI STATIC ANALYSIS: APP0-ADMIN"
echo "==============================="
code=0
export MYPYPATH=plugins/platform-auth/src:app0-admin/src/ && python3 -m mypy --install-types --namespace-packages --non-interactive -p app0.admin
export MYPYPATH=plugins/platform-auth/src:app0-admin/src/ && python3 -m mypy --namespace-packages -p app0.admin
code+=$?
python3 -m flake8 --max-line-length=120 app0-admin/src/
code+=$?
python3 -m pylint app0-admin/src/app0/admin
code+=$?
if [ $code -gt 0 ]
then
  echo "[FAILED] CI STATIC ANALYSIS: APP0-ADMIN"
fi
echo "========================================================================================================"
exit $code
