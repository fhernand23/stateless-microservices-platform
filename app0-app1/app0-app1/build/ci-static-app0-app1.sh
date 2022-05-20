echo "===================================="
echo "CI STATIC ANALYSIS: app0-app1"
echo "===================================="
code=0
export MYPYPATH=app0-app1/src/ && python3 -m mypy --namespace-packages -p app0.app1
code+=$?
python3 -m flake8 --max-line-length=120 app0-app1/src/
code+=$?
python3 -m pylint app0-app1/src/claims/attendant
code+=$?
if [ $code -gt 0 ]
then
  echo "[FAILED] CI STATIC ANALYSIS: app0-app1"
fi
echo "========================================================================================================"
exit $code
