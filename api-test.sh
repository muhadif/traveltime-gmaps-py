# Replace 'YOUR_API_KEY' with your actual Google Maps API key
API_KEY=env.API_KEY

# Sample coordinates
origin="-7.360161409,110.5115585"
destination="-7.363244982,110.4858699"

# Google Maps Distance Matrix API endpoint
endpoint="https://maps.googleapis.com/maps/api/distancematrix/json"

# Construct the request URL
request_url="${endpoint}?origins=${origin}&destinations=${destination}&mode=driving&language=en-US&units=metric&key=${API_KEY}"

# Make the GET request using curl
curl -X GET "${request_url}"
