# PowerShell script to set up automatic ML model training
# This script creates a Windows scheduled task to run the training script regularly

Write-Host "Setting up automatic ML model training..." -ForegroundColor Green

# Define paths
$scriptPath = "D:\mcpdocs\mcpwindows\train_model_from_logs.py"
$pythonPath = "python"
$logPath = "D:\mcpdocs\mcpwindows\logs\training_log.txt"

# Create logs directory if it doesn't exist
$logDir = Split-Path $logPath -Parent
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
    Write-Host "Created logs directory: $logDir" -ForegroundColor Yellow
}

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH" -ForegroundColor Red
    exit 1
}

# Check if the training script exists
if (-not (Test-Path $scriptPath)) {
    Write-Host "Error: Training script not found at $scriptPath" -ForegroundColor Red
    exit 1
}

# Define the action to run
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath -WorkingDirectory (Split-Path $scriptPath -Parent)

# Define triggers (run every 6 hours)
$trigger1 = New-ScheduledTaskTrigger -Daily -At "06:00"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "12:00"
$trigger3 = New-ScheduledTaskTrigger -Daily -At "18:00"
$trigger4 = New-ScheduledTaskTrigger -Daily -At "00:00"

# Define settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Define principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Create the scheduled task
$taskName = "MCP-ML-AutoTraining"
$taskDescription = "Automatically train ML models using Windows system logs for MCP Windows Automation"

try {
    # Remove existing task if it exists
    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "Removed existing scheduled task" -ForegroundColor Yellow
    }
    
    # Register the new task
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($trigger1, $trigger2, $trigger3, $trigger4) -Settings $settings -Principal $principal -Description $taskDescription
    
    Write-Host "✓ Scheduled task '$taskName' created successfully" -ForegroundColor Green
    Write-Host "  - Runs every 6 hours (06:00, 12:00, 18:00, 00:00)" -ForegroundColor Cyan
    Write-Host "  - Script: $scriptPath" -ForegroundColor Cyan
    Write-Host "  - Working Directory: $(Split-Path $scriptPath -Parent)" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test the task by running it once
Write-Host "`nTesting the scheduled task..." -ForegroundColor Yellow
try {
    Start-ScheduledTask -TaskName $taskName
    Write-Host "✓ Task started successfully. Check Task Scheduler for results." -ForegroundColor Green
} catch {
    Write-Host "Warning: Could not start task immediately: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Display task information
Write-Host "`nScheduled Task Information:" -ForegroundColor Cyan
Write-Host "Task Name: $taskName"
Write-Host "Description: $taskDescription"
Write-Host "Next Run Times:"
$task = Get-ScheduledTask -TaskName $taskName
$taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
Write-Host "  Last Run: $($taskInfo.LastRunTime)"
Write-Host "  Next Run: $($taskInfo.NextRunTime)"

Write-Host "`nTo manage the task:" -ForegroundColor Yellow
Write-Host "  View: Get-ScheduledTask -TaskName '$taskName'"
Write-Host "  Start: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "  Stop: Stop-ScheduledTask -TaskName '$taskName'"
Write-Host "  Remove: Unregister-ScheduledTask -TaskName '$taskName'"

Write-Host "`nSetup completed successfully!" -ForegroundColor Green
