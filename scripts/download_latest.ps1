# [c] jodua 20220616

# Download latest tweets using snscrape

# First argument is the hashtag
# Second argument is amount of latest tweets to download

$hashtag = $args[0]
$amount = $args[1]

function Find-SnscrapeInstallation() {
    $snscrapeCommand = Get-Command snscrape -errorAction SilentlyContinue
    $snscrapeCommandNotFoundError = "Snscrape is not installed. Please install snscrape before running this script."

    if ($null -eq $snscrapeCommand) {
        Write-Host $snscrapeCommandNotFoundError
        exit 1
    }
}

function Get-LatestTweets() {
    Write-Output "Downloading latest tweets with #${hashtag}"
    snscrape --max-results $amount --jsonl twitter-hashtag hashtag > "data/latest_${hashtag}.json"
    Write-Output "Download complete"
}

Find-SnscrapeInstallation
Get-LatestTweets