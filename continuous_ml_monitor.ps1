# Continuous ML Monitoring Script
# Collects system metrics and user activity data every 5 seconds

Write-Host "🔍 Starting Continuous ML Monitoring..." -ForegroundColor Green
Write-Host "📊 Data collection interval: 5 seconds" -ForegroundColor Cyan
Write-Host "⏹️  Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
Write-Host ""

$monitoringActive = $true
$counter = 0

# Function to get system metrics
function Get-SystemMetrics {
    $cpu = Get-WmiObject -Class Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
    $memory = Get-WmiObject -Class Win32_OperatingSystem
    $memoryUsed = [math]::Round(($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100, 2)
    
    $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DriveType=3" | Where-Object { $_.DeviceID -eq "C:" }
    $diskUsed = [math]::Round(($disk.Size - $disk.FreeSpace) / $disk.Size * 100, 2)
    
    return @{
        CPU = $cpu
        Memory = $memoryUsed
        Disk = $diskUsed
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
}

# Function to detect active applications
function Get-ActiveApplications {
    $processes = Get-Process | Where-Object { $_.MainWindowTitle -ne "" } | 
        Select-Object ProcessName, MainWindowTitle, WorkingSet64 |
        Sort-Object WorkingSet64 -Descending |
        Select-Object -First 10
    
    return $processes
}

# Main monitoring loop
try {
    while ($monitoringActive) {
        $counter++
        
        # Collect system metrics
        $metrics = Get-SystemMetrics
        $activeApps = Get-ActiveApplications
        
        # Display current status
        Write-Host "[$($metrics.Timestamp)] Cycle #$counter" -ForegroundColor White
        Write-Host "  CPU: $($metrics.CPU)% | Memory: $($metrics.Memory)% | Disk: $($metrics.Disk)%" -ForegroundColor Gray
        
        # Show top active applications
        if ($activeApps.Count -gt 0) {
            $topApp = $activeApps[0]
            $memoryMB = [math]::Round($topApp.WorkingSet64 / 1MB, 1)
            Write-Host "  Active: $($topApp.ProcessName) ($memoryMB MB)" -ForegroundColor Green
        }
        
        # Log data to file (for ML training)
        $logEntry = @{
            Timestamp = $metrics.Timestamp
            Cycle = $counter
            CPU = $metrics.CPU
            Memory = $metrics.Memory
            Disk = $metrics.Disk
            ActiveApplications = $activeApps | Select-Object -First 5
        }
        
        $logFile = "D:\mcpdocs\mcpwindows\ml_monitoring_data.json"
        $logEntry | ConvertTo-Json -Depth 3 | Add-Content -Path $logFile
        
        # Wait 5 seconds before next collection
        Start-Sleep -Seconds 5
    }
}
catch {
    Write-Host "❌ Monitoring stopped: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    Write-Host "🛑 ML Monitoring stopped at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
}
