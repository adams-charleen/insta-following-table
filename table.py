import os
from html import escape

# Read the results from the file
input_file = '/Users/charleenadams/scraping_insta/instagram_results.txt'
results = {}

with open(input_file, 'r') as file:
    for line in file:
        username, data = line.split(': ', 1)
        results[username] = eval(data.strip())  # Safely convert string dict to dict

# Generate HTML table
html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            font-family: Arial, sans-serif;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>Username</th>
            <th>Posts</th>
            <th>Followers</th>
            <th>Following</th>
        </tr>
"""

for username, data in results.items():
    posts = escape(str(data.get('posts', 'N/A')))
    followers = escape(str(data.get('followers', 'N/A')))
    following = escape(str(data.get('following', 'N/A')))
    html += f"""
        <tr>
            <td>{escape(username)}</td>
            <td>{posts}</td>
            <td>{followers}</td>
            <td>{following}</td>
        </tr>
    """

html += """
    </table>
</body>
</html>
"""

# Save the HTML to a file
output_dir = '/Users/charleenadams/scraping_insta'
output_file = os.path.join(output_dir, 'instagram_results_table.html')
with open(output_file, 'w') as file:
    file.write(html)

print(f"HTML table saved to {output_file}")
