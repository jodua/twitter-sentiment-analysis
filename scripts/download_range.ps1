# [c] jodua 20220616

# Download tweets between two dates

# First argument is the hashtag
# Second argument is amount of tweets to download
# Third argument is the start date
# Fourth argument is the end date
# Fifth argument is the interval between tweets in days

$hashtag = $args[0]
$amount = $args[1]
$dateStart = Get-Date $args[2]
$dateEnd = $args[3]
$interval = $args[4]


function Find-SnscrapeInstallation() {
    $snscrapeCommand = Get-Command snscrape -errorAction SilentlyContinue
    $snscrapeCommandNotFoundError = "Snscrape is not installed. Please install snscrape before running this script."

    if ($null -eq $snscrapeCommand) {
        Write-Host $snscrapeCommandNotFoundError
        exit 1
    }
}

function Get-Tweets() {
    Write-Output "Downloading tweets for hashtag $hashtag from $dateStart to $dateEnd with interval $interval days"


    while ($dateStart -lt $dateEnd) {
        Write-Output "=========================================================="
        $formattedDateStart = $dateStart.ToString("yyyy-MM-dd")
        $dateStart = $dateStart.AddDays($interval)
        $formattedDateEnd = $dateStart.ToString("yyyy-MM-dd")

        Write-Output "Downloading tweets from $formattedDateStart to $formattedDateEnd"
        
        snscrape --max-results $amount --since $formattedDateStart --jsonl twitter-search "#${hashtag} until:${formattedDateEnd}" > "data/${formattedDateStart}_${formattedDateEnd}_${hashtag}.json"

        Write-Output "Downloaded tweets from $formattedDateStart to $formattedDateEnd"
        Write-Output "=========================================================="
    }
}


Find-SnscrapeInstallation
Get-Tweets