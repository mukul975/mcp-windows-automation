# ML Stats Monitor - PowerShell Version
# Displays ML engine statistics every 21 seconds

Write-Host "ML Stats Monitor Starting..." -ForegroundColor Green
Write-Host "Checking ML engine status every 21 seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
Write-Host ("=" * 60) -ForegroundColor Gray

$iteration = 0

try {
    while ($true) {
        $iteration++
        $currentTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        # Clear screen
        Clear-Host
        
        Write-Host "ML Stats Monitor (Update #$iteration)" -ForegroundColor Green
        Write-Host "Current Time: $currentTime" -ForegroundColor Cyan
        Write-Host "Next Update: 21 seconds" -ForegroundColor Yellow
        Write-Host ("=" * 60) -ForegroundColor Gray
        Write-Host ""
        
        # Get ML stats using Python
        try {
            $pythonScript = @"
import sys
sys.path.append('.')
from src.ml_predictive_engine import get_ml_engine

try:
    ML_ENGINE = get_ml_engine()
    data_collector = ML_ENGINE['data_collector']
    behavior_predictor = ML_ENGINE['behavior_predictor']
    system_optimizer = ML_ENGINE['system_optimizer']
    
    print('ML Engine Statistics:')
    print('')
    print('Data Collection:')
    print(f'  - User actions recorded: {len(data_collector.actions)}')
    print(f'  - System metrics recorded: {len(data_collector.metrics)}')
    print('')
    print('Model Status:')
    print(f'  - Behavior predictor trained: {"YES" if behavior_predictor.is_trained else "NO"}')
    print(f'  - System optimizer trained: {"YES" if system_optimizer.is_trained else "NO"}')
    print('')
    print('Training Progress:')
    metrics_count = len(data_collector.metrics)
    actions_count = len(data_collector.actions)
    print(f'  - System Optimizer: {metrics_count}/100 metrics ({metrics_count}%)')
    print(f'  - Behavior Predictor: {actions_count}/50 actions ({min(actions_count*2, 100)}%)')
    print('')
    
    if len(data_collector.metrics) > 0:
        last_metric = data_collector.metrics[-1]
        print('Latest System Metrics:')
        print(f'  - CPU Usage: {last_metric.cpu_usage:.1f}%')
        print(f'  - Memory Usage: {last_metric.memory_usage:.1f}%')
        print(f'  - Disk Usage: {last_metric.disk_usage:.1f}%')
        print(f'  - Active Processes: {last_metric.active_processes}')
        print(f'  - Last Updated: {last_metric.timestamp.strftime("%H:%M:%S")}')
        print('')
    
    if len(data_collector.actions) > 0:
        recent_actions = data_collector.actions[-3:]
        print('Recent Actions:')
        for action in recent_actions:
            print(f'  - {action.action_type} in {action.application} at {action.timestamp.strftime("%H:%M:%S")}')
            
except Exception as e:
    print(f'Error getting ML stats: {str(e)}')
"@
            
            $stats = python -c $pythonScript 2>&1
            Write-Host $stats
        }
        catch {
            Write-Host "Error calling ML engine: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host ("=" * 60) -ForegroundColor Gray
        Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Red
        
        # Wait 21 seconds
        Start-Sleep -Seconds 21
    }
}
catch {
    Write-Host "`n`nML Stats Monitor stopped" -ForegroundColor Yellow
    Write-Host "Goodbye!" -ForegroundColor Green
}
