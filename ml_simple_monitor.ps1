# Simple ML Stats Monitor
param(
    [int]$Interval = 21
)

Write-Host "ML Stats Monitor Starting..." -ForegroundColor Green
Write-Host "Checking every $Interval seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host "=" * 50

$iteration = 0

try {
    while ($true) {
        $iteration++
        $currentTime = Get-Date -Format "HH:mm:ss"
        
        Clear-Host
        Write-Host "ML Monitor #$iteration - $currentTime" -ForegroundColor Cyan
        Write-Host "=" * 50
        
        # Simple Python call to get basic stats
        $result = python -c "
import sys
sys.path.append('.')
try:
    from src.ml_predictive_engine import get_ml_engine
    engine = get_ml_engine()
    dc = engine['data_collector']
    bp = engine['behavior_predictor'] 
    so = engine['system_optimizer']
    print(f'Metrics: {len(dc.metrics)}/100')
    print(f'Actions: {len(dc.actions)}/50')
    print(f'Behavior Model: {\"Trained\" if bp.is_trained else \"Not Trained\"}')
    print(f'System Model: {\"Trained\" if so.is_trained else \"Not Trained\"}')
    if len(dc.metrics) > 0:
        m = dc.metrics[-1]
        print(f'CPU: {m.cpu_usage:.1f}% | RAM: {m.memory_usage:.1f}%')
except Exception as e:
    print(f'Error: {e}')
" 2>$null
        
        if ($result) {
            Write-Host $result -ForegroundColor White
        } else {
            Write-Host "ML Engine not available" -ForegroundColor Red
        }
        
        Write-Host "=" * 50
        Write-Host "Next update in $Interval seconds..." -ForegroundColor Gray
        
        Start-Sleep -Seconds $Interval
    }
}
catch {
    Write-Host "`nMonitor stopped" -ForegroundColor Yellow
}
