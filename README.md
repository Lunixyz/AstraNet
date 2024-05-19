# AstraNet

This is AstraNet, my most ambicious project yet.</br>
AstraNet is a system focused on managing updates from Steam apps. It uses Discord as a way to comunicate, but being a BOT is not its main purpose.

## Engines
AstraNet uses three engines, they are internally called `rest_engine`, `data_engine` and `main`, but I decided to give them nice names, so they're `Radon`, `Neon` and `Astra`. Their purpose is as it follows:

* ### Astra (Main Engine)
    Language: <b>Python</b></br>
    Joins everything together and runs the Discord BOT.
* ### Radon (Data Engine)
    Language: <b>Rust</b></br>
    Manages, collects, analyzes and handles the raw data provided by <i>Neon</i>.

* ### Neon (REST Engine)
    Language: <b>TypeScript</b></br>
    Creates a bridge between Steam and <i>Radon</i>.


<i> It runs them using Python's subprocess lib. Not the most robust way, but it works.<br></br>
> This project is inspired by SteamDB. No affiliation of any sort to it though.
</i>