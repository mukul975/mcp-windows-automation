# Background ML Monitoring Service
# Runs hidden and collects data every 5 seconds

# Hide PowerShell window
Add-Type -Name Window -Namespace Console -MemberDefinition '
[DllImport("Kernel32.dll")]
public static extern IntPtr GetConsoleWindow();
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
'
$consolePtr = [Console.Window]::GetConsoleWindow()
[Console.Window]::ShowWindow($consolePtr, 0) # Hide window

# Create monitoring flag file
$flagFile = "D:\mcpdocs\mcpwindows\ml_monitoring_active.flag"
"ACTIVE" | Out-File -FilePath $flagFile -Force

# Log file for data collection
$logFile = "D:\mcpdocs\mcpwindows\ml_monitoring_log.txt"
$dataFile = "D:\mcpdocs\mcpwindows\ml_data_collection.json"

# Initialize log
"ML Monitoring Started: $(Get-Date)" | Out-File -FilePath $logFile -Force

$counter = 0

# Main monitoring loop
while (Test-Path $flagFile) {
    try {
        $counter++
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        
        # Collect system metrics
        $cpu = (Get-WmiObject -Class Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
        $memory = Get-WmiObject -Class Win32_OperatingSystem
        $memUsed = [math]::Round(($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100, 2)
        
        # Get active processes
        $activeProcesses = Get-Process | Where-Object { $_.MainWindowTitle -ne "" } | 
            Select-Object -First 3 ProcessName, WorkingSet64, MainWindowTitle
        
        # Create data entry
        $dataEntry = @{
            Timestamp = $timestamp
            Cycle = $counter
            CPU_Percent = $cpu
            Memory_Percent = $memUsed
            Active_Processes = $activeProcesses
            PID = $PID
        }
        
        # Log to JSON file
        $dataEntry | ConvertTo-Json -Compress | Add-Content -Path $dataFile
        
        # Update log file
        "[$timestamp] Cycle $counter - CPU: $cpu%, Memory: $memUsed%" | Add-Content -Path $logFile
        
        # Wait 5 seconds
        Start-Sleep -Seconds 5
        
    } catch {
        "ERROR: $($_.Exception.Message)" | Add-Content -Path $logFile
        Start-Sleep -Seconds 5
    }
}

# Cleanup when stopped
"ML Monitoring Stopped: $(Get-Date)" | Add-Content -Path $logFile
