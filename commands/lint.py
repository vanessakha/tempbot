from yapf.yapflib.yapf_api import FormatCode
import re


async def lint(client, message, params):
    # Turns the param list into one long string
    code_line = message.content

    # Regex pattern searches for code
    regex = r"((?<=(```py\s))|(?<=(```python\s)))([\s\S]*)(?=(\s```))"

    # Checks for regex match(if code is surrounded by ```py ``` or ```python ```)
    if(re.search(regex, code_line)):
        # Group 4 is what the code is, other groups contain the header tags.
        code = re.search(regex, code_line).group(4)
        # Uses yapf to format w/ pep8 linter
        try:
            formatted = FormatCode(code, style_config='pep8')
            await client.send_message(message.channel, "```py\n" + formatted[0] + "\n```")
        except:
            await client.send_message(message.channel, "Error in code.")

    else:
        # Invalid code
        await client.send_message(message.channel, "Invalid code, buckeroo!")
        print(code_line)
