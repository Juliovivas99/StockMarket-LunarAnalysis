# Azure Automation Runbook for Stock and Lunar Phase Analysis
# This PowerShell script runs the Python analysis script in Azure Automation

# Define variables
$pythonScriptPath = "azure_stock_lunar_analysis.py"
$reportPath = "lunar_stock_analysis_report.md"
$correlationImagePath = "correlation_heatmap.png"
$returnsImagePath = "returns_by_lunar_phase.png"

# Log the start of the script
Write-Output "Starting Stock and Lunar Phase Analysis at $(Get-Date)"

# Make sure Python modules are installed
Write-Output "Installing required Python packages..."
pip install pyodbc pandas matplotlib seaborn scipy python-dotenv tabulate

# Run the analysis script
Write-Output "Running the analysis script..."
try {
    python $pythonScriptPath
    Write-Output "Analysis completed successfully!"
    
    # Read and output the report
    if (Test-Path $reportPath) {
        Write-Output "Report generated successfully. Content:"
        Get-Content $reportPath
    } else {
        Write-Error "Report file was not generated!"
    }
    
    # Check if visualizations were created
    if (Test-Path $correlationImagePath) {
        Write-Output "Correlation heatmap generated successfully."
    } else {
        Write-Warning "Correlation heatmap was not generated!"
    }
    
    if (Test-Path $returnsImagePath) {
        Write-Output "Returns by lunar phase chart generated successfully."
    } else {
        Write-Warning "Returns by lunar phase chart was not generated!"
    }
    
    # Save the report and visualizations to a storage account (if needed)
    # Replace with appropriate Azure Storage Account cmdlets
    # Example:
    # $storageAccountName = "stockdatablob"
    # $storageAccountKey = "yourkey"
    # $containerName = "reports"
    # Set-AzStorageBlobContent -File $reportPath -Container $containerName -Blob "lunar_analysis/$(Get-Date -Format 'yyyy-MM-dd')/report.md" -Context $ctx
    
    # Send email notification (if needed)
    # Example:
    # $emailParams = @{
    #    To = "youremail@example.com"
    #    Subject = "Stock and Lunar Phase Analysis Report - $(Get-Date -Format 'yyyy-MM-dd')"
    #    Body = "Please find attached the latest stock and lunar phase analysis report."
    #    SmtpServer = "smtp.office365.com"
    #    Port = 587
    #    UseSsl = $true
    #    Credential = $emailCredential
    # }
    # Send-MailMessage @emailParams
} 
catch {
    Write-Error "Error running the analysis script: $_"
    throw $_
}

# Log the end of the script
Write-Output "Stock and Lunar Phase Analysis completed at $(Get-Date)" 