# shaarchiver
Archive your [Shaarli](https://github.com/sebsauvage/Shaarli) or [delicious](https://delicious.com) bookmarks.
Status: **draft**. Use at your own risk

 * Supports local Shaarli/delicious bookmark exports (Netscape HTML format)
 * Supports downloading exports from your own Shaarli install
 * Downloads all linked media for archiving, backup, offline use...

### Installation
 * `git clone https://github.com/nodiscc/shaarchiver` or download and extract the [zip archive](https://github.com/nodiscc/shaarchiver/archive/master.zip)
 * install the required python modules: `python-bs4 python-requests`


#### Usage
Edit the config variables at the beginning of bookmarks-fetcher.py if needed.

    ./export-shaarli.py #download HTML export from your shaarli
    ./bookmarks-fetcher.py #download and archive pages/media in your HTML export

```
 ↳ ./export-shaarli.py -h
Usage: export-shaarli.py [options]

Options:
  -h, --help            show this help message and exit
  --username=USERNAME   username for HTML and private links export
  --password=PASSWORD   password for HTML and private links export
  -d DOWNLOADDIR, --download-dir=DOWNLOADDIR
                        destination directory for bookmark backups
  -u URL, --url=URL     URL of your Shaarli (https://my.example.com/links)
  -t TYPE, --type=TYPE  download links of TYPE (public, private or all)


```

```
 ↳ ./bookmarks-fetcher.py -h
Usage: bookmarks-fetcher.py [options]

Options:
  -h, --help            show this help message and exit
  -t TAG, --tag=TAG     download files only for specified TAG
  -f FILE, --file=FILE  source HTML bookmarks FILE
  -d DIR, --destination=DIR
                        destination backup DIR
  -m, --markdown        create a summary of files with markdown
  -n, --no-download     do not download files

```

#### Bugs/feature requests/discussion
 * https://github.com/nodiscc/shaarchiver/issues/

#### Example output directory
Here is what your backup directory should look like after archving some links:

```
~/git/shaarchiver (master *=)$
▧ tree backups/
backups/
├── audio
│   ├── music
│   │   ├── blues
│   │   │   ├── American Woman The Guess Who-e8z1EzDouNs.m4a
│   │   │   ├── Emancipator - Dusk To Dawn-CP7VcsaoqZc.m4a
│   │   │   ├── HOWLIN' WOLF - HOW MANY MORE YEARS - LIVE 1966-p7LElLVani4.m4a
│   │   │   ├── Jimi Hendrix - Rainy Day Dream Away, Still Raining Still Dreaming (with Lyrics)-rAMtbQwkfog.m4a
│   │   │   ├── Lightnin' Hopkins  -  Stinking Foot-eVXoWxBL8EA.m4a
│   │   │   └── Motörhead - Whorehouse Blues (Music Video)-y0sik4yZHY8.m4a
│   │   ├── electronic
│   │   │   ├── Beat Torrent - 01 - No One Knows-CsaKF-QbslQ.m4a
│   │   │   ├── Covert - Dépêchez-vous [New Talent] FREE DOWNLOAD-_mECfFcCbuo.m4a
│   │   │   ├── DVA - Eye Know Featuring Natalie Maddix ( Hyperdub 2012)-jZI2i0IQk8s.m4a
│   │   │   ├── Falling Into Place-180901007.mp3
│   │   │   ├── High tone - Rub-A-Dub anthem (Feat. Pupajim)-lKj852Cm_pU.m4a
│   │   │   ├── Igorrr - Tout Petit Moineau @ Dour Festival 2014-1Rk1K5Mmnbg.m4a
│   │   │   ├── Marijuana-53126096.mp3
│   │   │   ├── M.O.O.N. - 'Hydrogen' [Hotline Miami Soundtrack]-SNE2oCZH_4k.m4a
│   │   │   ├── MUSCLE X ROBERT PARKER - HONOLULU ICE-178918540.mp3
│   │   │   ├── November-179398279.mp3
│   │   │   ├── One Night  in  MIAMI LIGHTS-145544423.mp3
│   │   │   ├── State of Mind - Real Mccoy (Black Sun Empire Remix)-KsZyfCUcdhw.m4a
│   │   │   ├── Stevie Wonder - Superstition (C2C Remix)-1TX5gsKBo88.m4a
│   │   │   ├── The Subs - Mitsubitchi (Original)-sat9d69b7lI.m4a
│   │   │   ├── Trinity - Jah-xDVcL-CNXRQ.m4a
│   │   │   ├── Trip Hop Mix The Best Of 2014-svqbb387fVw.m4a
│   │   │   └── Troy Samuela - Yams-182217601.mp3
│   │   ├── hiphop
│   │   │   ├── Die Antwoord 'Dis iz why I'm hot' Studio-X Remix HD-0nfWxVdXuCw.m4a
│   │   │   ├── Digable Planets - Where I'm From-SMvFRpMCyRI.m4a
│   │   │   ├── [GTA IV Theme] Micheal Hunter - Soviet Connection (HQ)-8t_ZH2Iaa8Q.m4a
│   │   │   ├── Jesse James - 50's Manhattan-qP5WAMgEJ4E.m4a
│   │   │   ├── Karamel Kel - Poetic Symphony-W5KEnS5lRFA.m4a
│   │   │   ├── P.R - Long Walk-ed9Hl_fei3U.m4a
│   │   │   ├── Roger Molls - What's your place (Instrumental)-eOp4vU4yzRM.m4a
│   │   │   ├── Souls of Mischief - 93 'Til Infinity (1993)-mVDEdxpqZgo.m4a
│   │   │   └── Void Pedal - Pair-5kePk_OHHlc.m4a
│   │   ├── other
│   │   │   ├── At the Nines-188043845.mp3
│   │   │   ├── Autumn Bliss-2390009158.mp3
│   │   │   ├── Blossom-298549791.mp3
│   │   │   ├── Darling-2270153745.mp3
│   │   │   ├── Day By Day-2526218355.mp3
│   │   │   ├── Dean Martin - Let it Snow!-mN7LW0Y00kE.m4a
│   │   │   ├── Delight-299902498.mp3
│   │   │   ├── Deus Ex - Human Revolution Soundtrack - Adam Jensen's Apartment-2cIbVP0W0y8.m4a
│   │   │   ├── Diplo - Revolution (L Y N X Remix)-189226827.mp3
│   │   │   ├── drown-3065028236.mp3
│   │   │   ├── DVA - Nunovo tango LIVE on Dnipropetrovsk TV-n5tCgQwW-9I.m4a
│   │   │   ├── E X T R A-177357744.wav
│   │   │   ├── Feel Good-1257634034.mp3
│   │   │   ├── Feelings-165404455.wav
│   │   │   ├── Float-1889744020.mp3
│   │   │   ├── Folklore-3748247179.mp3
│   │   │   ├── Forever-460349760.mp3
│   │   │   ├── Fragment-3263034211.mp3
│   │   │   ├── Fulfill _ The Dream-3416690747.mp3
│   │   │   ├── Hello World-3412928147.mp3
│   │   │   ├── heRajiKa tracks - Wayfairing Stranger-GOlOP70Somc.m4a
│   │   │   ├── Intimate-637311741.mp3
│   │   │   ├── iZem - Sadeo (feat. Feather)from the forthcoming album 'Hafa'-179018983.mp3
│   │   │   ├── John Beltran -- Bota Foga-7qtqdZ-3-VY.m4a
│   │   │   ├── Long Arm - The Roots-EY4bR5vwtsM.m4a
│   │   │   ├── Miles Davis - Boplicity-HLzqjmoZZAc.m4a
│   │   │   ├── 'Moon' Little People-IK5I4cTkL-E.m4a
│   │   │   ├── mr. Gnome - House Of Circles-rQ5uxrhBz9E.m4a
│   │   │   ├── Pharoah Sanders - Equinox-bOQz1R9dF1A.m4a
│   │   │   ├── Pharrell Williams - Happy (Official Music Video)-y6Sxv-sUYtM.m4a
│   │   │   ├── Portico Quartet - The Full Catastrophe-Qpyb6f5_uTg.m4a
│   │   │   ├── radionova-high-radionova-high.mp3
│   │   │   ├── Ratatat - Loud Pipes [HD]-iexoDhvwGbo.m4a
│   │   │   ├── Reverie-2807407651.mp3
│   │   │   ├── rinse-3619491339.mp3
│   │   │   ├── Serenade-2605211418.mp3
│   │   │   ├── Serenity - Resident Evil 4 Music Extended-r3SwvRntnyA.m4a
│   │   │   ├── Sky Blue-345381572.mp3
│   │   │   ├── soak-136957250.mp3
│   │   │   ├── Songs We Danced To-1129346456.mp3
│   │   │   ├── The Kilimanjaro Darkjazz Ensemble - Shadows-MnrH-7URvpc.m4a
│   │   │   ├── Thousands of Rhythms-3648242690.mp3
│   │   │   ├── TOKiMONSTA - Fool-VJogmBeu2lY.m4a
│   │   │   ├── Tribute to Music-65774836.mp3
│   │   │   ├── Wanderlust-2922440868.mp3
│   │   │   └── wash-1820898041.mp3
│   │   └── wtf
│   │       └── the proclaimers_500 miles-tM0sTNtWDiI.m4a
│   ├── other
│   │   ├── other
│   │   │   └── Train Driver's View - Halmstad to Göteborg-1Rq9b_bn6Bc.m4a
│   │   └── samples
│   │       └── Train Driver's View - Halmstad to Göteborg-1Rq9b_bn6Bc.m4a
│   └── video
│       ├── films
│       │   ├── Die Hard - Joyeux Noël-2TbzjYhN470.m4a
│       │   └── Léon - Gary Oldman-6f_ErGfv65U.m4a
│       └── samples
├── links-2015-02-20_2349.md
├── links-2015-02-21_0108.md
├── links-2015-02-22_1952.md
├── links-2015-02-22_2235.md
└── media
    └── video
        ├── documentaire
        │   ├── Démocratie représentative-W3JO71qNXeU.mp4
        │   └── FSF_30_720p-FSF_30_720p.webm
        ├── films
        │   └── Straight Outta Compton - Red Band Trailer with Introduction from Dr. Dre and Ice Cube (HD)(Official)-OrlLcb7zYmw.mp4
        ├── games
        │   ├── No Man's Sky at The Game Awards _ PS4--X8KMoAWFPE.mp4
        │   ├── video-{{meta.unknown_video
        │   └── World Premiere - Adr1ft-0sl8t7qGQRs.mp4
        ├── news
        │   ├── Charbon  - le fossile qui a de beaux restes #DATAGUEULE 16-kk0TIhy2D3g.mp4
        │   ├── Le Zapping - 03_01_15-1191980.flv
        │   └── TAFTA ta gueule à la récré #DATAGUEULE 14-zHK1HqW-FQ0.mp4.part
        ├── other
        │   ├── DEX UI Demo-117199764.mp4
        │   ├── insomniac（2008）-24162153.mp4
        │   ├── Le Zapping - 03_01_15-1191980.flv
        │   └── World Premiere - Adr1ft-0sl8t7qGQRs.mp4
        ├── shortfilm
        │   ├── 'The Ancestor' by Darlingside – Official Music Video-50507428.mp4
        │   ├── Time Trap (Short Film)-BpmkpCK3ysg.mp4
        │   └── Wake Up Call-jid2A7ldc_8.mp4
        ├── space
        │   ├── Astronaut - A journey to space-111049676.mp4
        │   ├── GoPro Hero Camera Captures Awesome Sight Of Antares Orb-3 Rocket Explosion-t1j9TEiqaXM.mp4
        │   ├── Neil deGrasse Tyson - We Stopped Dreaming (Episode 1)-CbIZU8cQWXc.mp4
        │   └── Wanderers - a short film by Erik Wernquist-108650530.mp4
        ├── technology
        │   ├── Replay of Vega liftoff VV04 with IXV-nqggvBGLPPw.mp4
        │   ├── Samsung  - trois étoiles et des poussières #DATAGUEULE 17-tYk_elaPDIY.mp4
        │   ├── Staying Dry in a World Covered with Water-7nD7gr1NIf4.mp4
        │   └── Tim Tyler - My keyboard-9yg3s77nAMQ.mp4
        └── wtf
            ├── Bob explique la Guerre contre l'EI-fgRu.mp4
            ├── Charlie The Unicorn Goes to Candy Mountain - CandyMountain-_yJCNNwHUOE.mp4
            ├── Front Load Washer Total Carnage - Washer goes Chain Chomp on me-dq6T5BojXc8.mp4
            ├── GIF-JAM 2014-112952764.mp4
            ├── Heaven's Countryland - US Americans Part 7 - Pharmaceuticals-107202823.mp4
            ├── How round is your circle!  www.howround.com-270qEZKXAfQ.mp4
            ├── L'ami du petit déjeuner  - l'ami riCoRé S-wYLEZ0mUfI4.mp4
            ├── Le merveilleux monde des Cuys-112061208.mp4
            ├── Les images saisissantes du crash d'un avion de la TransAsia à Taïwan-x2gdgfg.mp4
            ├── RC Plane's First Flight-jjzjcIE5oUM.mp4
            ├── Staying Dry in a World Covered with Water-7nD7gr1NIf4.mp4
            ├── Tim Tyler - My keyboard-9yg3s77nAMQ.mp4
            └── Uh Buzz We Missed The Truck.-JL6RQdDh0mk.mp4

24 directories, 124 files

```