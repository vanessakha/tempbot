from yapf.yapflib.yapf_api import FormatCode
import re
import jsbeautifier
import discord


async def code_format(client, message):
    # Turns the param list into one long string
    code_line = message.content

    # Regex pattern searches for code
    pyRegex = r"((?<=(```py\s))|(?<=(```python\s)))([\s\S]*)(?=(\s```))"
    jsRegex = r"((?<=(```js\s))|(?<=(```javascript\s)))([\s\S]*)(?=(\s```))"

    # Checks for regex match(if code is surrounded by ```py ``` or ```python ```)
    if(re.search(pyRegex, code_line)):
        # Group 4 is what the code is, other groups contain the header tags.
        code = re.search(pyRegex, code_line).group(4)

        # Uses yapf to format w/ pep8 linter
        try:
            formatted = FormatCode(code, style_config='pep8')
            encoded = "```py\n" + formatted[0] + "\n```"

            # Put inside an embed to look nice
            embed = discord.Embed(title="Formatter",
                                  description="Python", color=0xda66a5)
            embed.add_field(name="Code:", value=encoded, inline=False)
            await client.send_message(message.channel, embed=embed)
        except:
            await client.send_message(message.channel, "Error in code.")

    # Checks for regex match(if code is surrounded by ```js ``` or ```javascript ```)
    elif(re.search(jsRegex, code_line)):
        # Group 4 is what the code is, other groups contain the header tags.
        code = re.search(jsRegex, code_line).group(4)

        # Format code with default jsbeautifier options
        formatted = jsbeautifier.beautify(code, jsbeautifier.default_options())
        encoded = "```js\n" + formatted + "\n```"

        # Put inside an embed to look nice
        embed = discord.Embed(title="Formatter",
                              description="JavaScript", color=0x0099cc)
        embed.add_field(name="Code:", value=encoded, inline=False)

        await client.send_message(message.channel, embed=embed)

    else:
        # Invalid code
        await client.send_message(message.channel, "Invalid code!")
        print(code_line)
