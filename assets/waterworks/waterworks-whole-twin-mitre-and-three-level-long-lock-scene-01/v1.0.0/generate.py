"""One static canal-lock exterior scene and zero new independent models. Two complete qualified balanced twin mitre gate modules retain every original mesh, raw GLB buffer, material dictionary and internal node hierarchy at original unit scale, with only separate longitudinal translation wrappers. New scene-only geometry joins their short mouths into a long narrow chamber between continuous outer banks, with a grounded slab and three separate opaque water-appearance volumes at distinct fixed levels. The upstream approach, enclosed middle chamber and downstream approach are visibly divided by the two intact angled gate pairs; original balance beams and pivot fittings remain intact above the banks. This is not a second gate counted as a new model: the scene relation is a long intervening chamber and two external approaches on a connected bank-and-bed layout, unlike the old single dry sluice/wheel race equipment scene. Water appearance deliberately stops short of reinforcing rails and leaves small wall clearances; it is not a sealed fluid simulation. No gates are cut, pivoted, scaled, recoloured, or extracted from their original mouth modules. No hydraulic operation, filling, flow, navigation, boat clearance, gate compatibility, watertightness, walkway access, load, engineering, installation or safety capability. Rigging, animation and interaction not made or verified."""
import base64, copy, hashlib, json, math, struct, zlib
from pathlib import Path
ASSET = 'waterworks-whole-twin-mitre-and-three-level-long-lock-scene-01'
TITLE = 'Whole Twin Mitre and Three Level Long Lock Scene'
TOL = 2e-07
INPUTS = {'uppergate': {'bytes': 45236, 'sha256': 'fd92505c11a7de3706cc854d8971e260b7ee6425c5b6a835a50cfac282c680cb', 'compressed': 'eNrtnH2QVNWVwC8IgigIyKcIwsRE0GZ83x/I9OVLYCIfyocmKxobaGBWmMFhUCNF1mJjZUUDW1krEWJ0a80mbBKNVGFBVKaJqWQ3LFpJ1ooby4ohVZvsRmuL1GaTrbhx95zX7/Tc7j6333s8susfQ6Vv/3xz7j3nnXvevfd098nW7euWDhVCHHteiCOLhfjo2tWr9rSVdu0q97XN29O2tdxd7i319fS2zWu7eVtvT3fPrplbocvMRdvL3ZvLvTM7b1g98z6n3W53/LZC233l3l1dPd0gbLUbbXsLbbs2wQBt84yYdrXNu2NPW3dpB1xrWxv9rdDW3bM5+oNRMAtWwS44BbfgFfxCUAgLJlw0C6ZVMO2C6RRMt2B6BdMvmEHBDAuWUbCgj1Ww7ILlFCy3YHl37r1zYMg9bTvKu7ZF+mOlt2/r2V5eu62nt2/1znL34lJ3afvKnt1928BYEjbrhVd29fWWNy8r9ZVXlEtbVpS39CmyVr3sbeXevq5Npe3Ly+Xtt3Td19PXIG7Xi6/fubPcG8mtKfeVusDVDfJOvfxHSzs2VsV7moZ260VX9HRvxdssLyptL3VvKi8ql3Y09PDqeywtbSov7+nterCnu6+0fU2pazvKG0oHP00HU+kQNHdY0lXa2gNOX9QL/9FgUFgvvq5n51K4z/tLn7wFbuGeRmtMI1FctcU0E8UtVdxKFLdV8YaZjb2+rLdrZ8NNmk6r8FrTtXVbnbSbEGBNHbykEGvq4bcIsibhIDnMmvqESXET9VDn1jJSdVHn1zITgq3RLKv1DDfbZCfL1xnkJMurEWe5yfJqyFmeNuTiW4WFcAfEVW9XaXt1Mdzcs3sjrH5dm8ub2+b19e4u10YYWAjX9vVEq/LOjb0rIWK2b+/atKZn99ZtsHjvwh1hY2lXeXHP9p5ecHC0L9xhtDu2Ef3zTddyXd8psJdsv3rJ8b3A9nEdRwNjHTQaTHwvqatdaw/C6J/vmW5gOpa5F92gv5vomYLH6b7yroXdm2PHrOvasbHcm/HOrFiz6bmu7YS+DfdhutVrnmPZvmXiJcNz6g3Mcm9W1DWwbdPwwtBNuDdcKaLHE29tbV9vaeeuTtiXM96XacYetU3fD40wxPsK6qbM9qNr9Z7n76vdrQ4XGKHluSb05G7UdaPhQbUFcuHeKD4hlOtPBboNeiUGPdxkb9eOrr6u++JOpb6+3q6Nu/vK0Z3esnpt57rO1asiV69avWblwhWw/MAxpKt7c9cmlLEGHgkQ2nsn+rr1Zp9Nrz2g11H1uqpes1kve3DIptobUO2rqgNVtdWsmj+EZNMdKu42sihvOtFk04ubek2xpSrGDbmlZt0BKaMBjmKAW2eAlzDlmvNWRv2+oj/Q67fS6jcz6ldm3jIy6286DWbTbinTb9VNv5U0/dzhMqNyZeotN8vDzp1UM+pWHnbLz6nbyqg7UHSHOXXbGZdXZV23zSy6Gw7kGdVailpbVWs7CXHGHO8z6nYV3V6dbj/rpnI+6pXZtsN8+8p5qHeUCXfM895ZzkezMueOnXtrOR8LlAXGqVtgnOx7SzWdyWiAsrk4gd4AK7UBGZc5R9ldXCOzAc3pXzb1rrK9uHXbi5txezkf77vK9Lt59pfz8byrbDCun1d5xh3GVdYcN8yrPOMW4ykrjne+W8x5BJunrDdewh4DiVNpE/xtV09vddCNu7dsKffe1lW+P0p9NvXs2AlZfHffuk/uLGMc43lhU8/u7j4YOxrtAehmtgfVjMyyA8cMwOtmu2c0XrFcTNO6uqHD3OYeRmFuLNIXqWq77abF1Q8pVJPMZJNadbe47natu4nbc9x/7eKFKxauaRrBbm2AVfOJAXfshFUnhK7t+Q4MznwMoPrENap/NBzPtlwvYFPpuUa7Ezs3sB3Hcw3LT/Cak2x0q+5ua6/ZXpLTvNb6w4CcBj5wzOgDEA+CwoY7s8GNvtfwmQC4wDbcuk+F6tzoREO4vhGAe9zIjVVpww09cK7jBJEb7foYTPCin3wXrboHCbEXJsZemMGNtl8NJdeyTc8KHHRj/RULXWBVP0kzDd8KAtszvDo/VmPPsUITYhU/smn3nYaIjqKxOnAQGH4IE5L0CBv5/GiaaR9BjKbqR0XqLXhVPzi+6/ghdsRoij/EArf4IFXnBd9yGxayJr+gE+LPrbwg8EI/MBMXMivfM2naeR9K00ntR6PdsGAtw48mbRMWST+0Hc6TEE8OeMT3PNv3DPCWpTyXVrvrwwIHz5wPAr4FFjIrJOgKqmM4sFQGLjywSZ50c3rSy+1JP4snPRtWLM8Gtzl2aIbRR9z1XjDRkzYEmOEbrgVvJjyhakg6pom9HR/eYSgcwahb39zo2faiETwDIhc8byftEmaQ05FhLjfA7m9G92AHJiwpvuVn9ILZbloN3wuchxcsI58XrITlybZVLwQWTFkIEwYPDGDkBcsyA3jYAj90YOlxo0MDPGqeaVl+ENqBFdYdGmwUhHsOTd90HB93O8eFFQgetcB2A9vwwsgPdnUMF3ZTz3TNRD9YyffRsn/CAuUESY+VlWmB8kIbzkzwP9jzYXXBvao5nKwAliob9n/ftnF9URZ6+CM4HR4/H9Z/WMe9sLrEOU17pmGZZgiDGOBaF0I3SDo4WDlXKMvL4AjbjhxhGTDL+F0L7wgTNnv4n20HBqy6pq36wfUiP7iuGXrwd0/jBgjHEIaAjc+ywJ9h0r5v+Tm9EGTwgmdEXvDgMAm7dBjyXjACeNLACz7sSLbvBJbqBnxycDXG5y4IHVvjBrx5DCk3WqCMMDEYwnxusI0MboClAd3gWDBLjh3tuE1uwIiGIIa5hi0bv3H0AqMuU4MO0XPheXCPLvTgHWHD4RzGgNby/cBLTOVsM6cjEhYof8ARFj74UcIUrYdBgE9FWD2xDWQJGDZudF++aQeh76tusNrt6lHShCOu7QTRftPwXS2OUH9a9MMkJ9jJN9Gyv5OQVThOYkbrpg0oJkHNmOMaFyqjtb2cwePnPfTZQdpsjElIM+a0TFZ8YVJaO8yXizlGBicw2WSmjJRPavMnpI6Z0wlW+geoOZnMlI6yCe2FSEcdO9/z5KQ+q7FpYKZMUpONXoBU0sl5UHNyp5KOnz6WmCwwSx6pSUUvQCLp5EwknfD8nZAti+Tz0AuRRro500g3KY00B3zQlAFmTCK5PPTCJJGulXwXLfvnTiLd1AsTnwBmSiLZNPSCpJBuzpXJ9dK7gcn/smSQbAp6IRJIN2cC6QbpfcAkf5nyRzYDvRDpo5szffSM9Gsrk/hlzB7ZDPRCJI9ezuTRS508solfptyRzT7zp45e1tQRxhvor37bG33Tu/GT+MOi7q19WJ4BmV10YfWWLVH5Dvy9r9S7FRESOs8asCW5b3QhbW8Lv8FVe8OR1qvvbrfqHjQox2Qzg/bG7pYRZDAelvv63rCZprfdNFG6rr/jZNDe3B+eJyd9fwi7+u5Ok++yme+agZPHfFxScsyd3xQ52boHWZzXOPWBiV/wnXfYBplc19zd8a0ctvuekcf2wLZy2A7pX55Zh4NwkKc7nGszPDJhQ8hCxu3k6G7Cxprh5pu7+36uxdII/DxTZ5pmricWzg9OkKu/n+uRh8iznFz9bTOX/yDJzOU/uJLBf0FTf9v0vTz9HcPL5T8ndPOsmqZrObn857pWju0eT3K59nsYIMi14Zt+pglgBggyeZAZIHRML9eByw2tnAe2XAc+WMKCXP0d18txYjR9x8nxBFhmkM/9lmk4ufrb+abP8rJMn93kPyvMMn3N/W3bybEBw4E/17EPUr9cpxd4eMNc0+/Yuc6dluPlOkBY0CHX0wsbQC7/uflyBsvNlDQ0baCWZ2Y5QDT3x+/OGvvX0v445VdvwIch9t65d+a57UIs6lwlXj3zbkVE//5apuCKjoU4lcSykQ8fmlpsxTh+AldUVvpqGeVfPXNG0jgco3wGruhYGVPLIC8VX3EsG1nxVRJXdAw2SGUek1i2YmVeOK6ojDYoPmQZ5TNwRcfKmC2Y/j0U39NDlfp39V/j39LI6MZvut7w3iij09XShoQxW9mV2rbKecj8MfxWuTB6W/oqQUZ37x9c/w8Rw8QIaEeIS+C/RopR0I4So8VF4nIxDtpx4mIxVIwRY6EdK4aLiWKKmAbtNDEDpEaJydBOFhNAerq4EtoroccYMUlcDe3V0OMycYW4CtqrxFTQMELMgnaW+JC4VHxYzIZ2thgPWtvENdBeA+NdDP2vhfZaMROkZonrob1etIPEXGFAa4DUTPirBa0lrhM3iIKwobWFKVwRiBuhvVEUQcoQPrS+cEC6Q8yDdh70+IjwhIRWijnQwxbzoZ0vQvHcsm9X3r01KM7ZcLBfx+gv5LMPPl5M4ueWne3QMY159cPv9LfiNSf6JdnAMY6JTHpbMdnAMY2p6m1kNW4+8fqx6L8/9VAPsy41PyP18nXjFOPrzDPCyrBrQII9MoU9MoU9spU9F8HrEnguLoNn4BKIX3x+xsN/D4FnZhy04+A5GQYxPgHaCfBcjIBYnwTtJHg+Lo2esEvhNVl8eefJ6KwC7/0nZryQyG+eqvJ7hdNaPnjgeMS/+6/XtXxg4YsRn7nhLS2TbWtO/FTLLz59qiav42+t+U5Nr467Z363Zr+OD77y3ZofdEzyK489r2XSe+u//q2Wyf49R5/SMvnht7Of1DL5E+V1TPOCenVM84v26xjjZMPBn0uKGY5RHplihmPUi0wxwzHaj0wxwzH6AZlihmP0J8nrGOeF9OoY55fs1zHGCflBxyRPMcMx6aWY4Zjsp5jhmPxAMcMx+ZNihmOaF4oZjml+KWY4Jr3oh+YzSpWPTNgTrYu7/35ZUeE6+X97c110ffm8MRWdDPxNxrIVVV6VQR2xzooqr5MhHcgNMv3KOBVuHPU6/a3RHvU66Wi8L+V6USejjCNVeY09UpXX3JdU5TX+kaq8Tkbxs9TMl1TmS2rmXapxou6nCfEjU8SPTBE/MkX8yBTxI1PEj0wRPzJF/MgU8SNTxI9MET8yRfzIFPEjU8SPTBE/Mm38CDhPDYF2BLxj5jIC2tFRFjMW3gWcrsZCi6csARnIJGgxExGQm1wFbRu8C8hE2qCdDe8Cco3Z0LbDO+ZG7XCO8yBLuAhOdB6c5ELILobD+S6Ek9x8yDZGwnlvPpzcipBz4PmtCKe+hZBbYO60EM5/S8QiaCfA+0SxTNwE7WR4nyJuFsujPOpmyJdWiY9COwPep4tbxUpoZ8H7TLFO3ALtNfD+IXG7WAvttfD+EfFxcRu0c+D9OrFB/Am0BXifKz4h7oT2Bng3IM+5G9qh8G5C/lOClw+tDxlQCV4d0HaIBdAuEIuhXSyWQrtUdELbKVZAu0Kshna1WAPtGrEe2vXiY9B+TNwB7R3iLmjvgrFL0XkV9u1oj3jjmecTeemXjkb82MgfavmJTccifv3LZ7X8tf0nIp7e/66WybY3njmn5adue6Umr+Pn936vplfHQ5d8v2a/ju/tOF3zg45J/qV//jstk95d8w9pmey//kMHtEx+uLdjv5bJnyivY5oX1Ktjml+0X8cYJ1u2/KIWMxyjPDLFDMeoF5lihmO0H5lihmP0AzLFDMfoT5LXMc4L6dUxzi/Zr2OME/KDjkmeYoZj0ksxwzHZTzHDMfmBYoZj8ifFDMc0LxQzHNP8UsxwTHoHz6uD59XB8+rgefWDeF599cxbFViv5ag3nunX8b0dLyYyyXeMekPLJN+KUR7ea2NyjPJJTPLqmI1M8q044/dxab6XOY/v7P5Pv6/J9P3dkOiT4yHwGgb5zVjIaEbH2Q1+4izgdRnkKvjJ88XwuiT6ZHkCtBMgVxkOOcpkaCdDdvL06UMn8bP9e+bvKer4+MgzLyP/5LVfdeh43BOzTiEf2/axio7Xv3ZNxLv/w9My6sUYIBs4Rr3IZAPHqBeZbOAY9SKTDRyr83Dgve7I/08dOF6EV796jWTwb/H1iirfQoau9TfI1MZnZGQKe2QKe2QKe2Qre9J93zECInNYlIOPjGJvZPRd4agoKkdF3xM+MPXoyVfPnCn+5rVDRR2/NHVfxG/evlvL7ktH8TcVxSvWPdyvY/PrxyKesnGFllHv8rO/r9nAMepFJhs4Rr3IZAPHqBeZbOC47my2r/p91S/+4VgRXv3qNZLBv8XXK6p8Cxm61t8gUxufkZEp7JEp7JEp7JGt7MF5mbPhoKQ54hjnBZnmiGOcF2SaI45xXpBpjjiuxslhORAzzVyNk8NyIGaauRonh+VAzDRzNU4Oy4GYaebB+GkdP/Dcn3zr1XeL/3Omu6jjR/f/+qS15VfF+Y88pmWUX3z8/eKvf/y5VDzm8iMn7zsoZNe2PVqes+GblR0bviC/+WBvfxoefuRoZd8rn5eeuzwVY9/v/fiL8h8P3ZiKV459tnJ055PyprfLmRnv/eAr/1k8MePh6L4OHzoE573b+1V++Deni199/PWOvoe7KqPfWys/e9e5/unvPFlc8NvT/X96/92VL9z6aL96HeT7Qf4kyEtVBrgILIGLX/vd6eLvH7hb9t30aFHXV9XbQr4m02BPBWSKINN//L/XVnruPlfsePvJfp1tOnnVZrVvi/FVe3T3y/ZV70snMxT28fGwT4+HXXoY7PCToJ0Eu/oI2MenwX5/Jez1o+LP2keLqWIGnACGQDsS3mfAqWAktEPg/Wo4F1whZsKuPwV4srgKeDqcB+760eP9W7b8WB55pK+o433luREfnvM5Lfvvf/Yk8pTnfjBfx+uLiyP5zqeefVnHqHf52TdrNnCMepHJBo5RLzLZwDHqRSYbOFbX0j/7QfUM9i//3i3hVXeNZPBv8fWiKt8wTjG+XlHlW8g06pIp7JEp7JEp7JGt7PnlZy6v4NwNW3VZUcfWuZ9F8/uXk+dr+f2Xn4341M1PntTxF996J+Kf/PQ9LaNenDuygWPUi0w2cIx6kckGjlEvMtnA8WD8tI6fp7+yLoqTT3eO7dDxDz/vRvzm8a9qOfjDtIj/vOT16/ji0TdGPPb6LVpGvTh3ZAPHqBeZbOAY9SKTDRyjXmSygePB+GkdP9/4+WPR3D285i9O6viRFx6M+Ogf/uZlHZ+bVor4r1Yd7Nfx2xMfivjj9le1jHpx7sgGjlEvMtnAMepFJhs4Rr3IZAPHg/HTOn7OPjjhlG3/k3zjGaNyb8f4RF6yv8onZrhanrPhiohv3hJomfQePhRq+fChiTV5HX/qnkk1vTpec2JSzX4dk/xvZxe0THo3nZ2tZbJ/wnPXapn8gPI6Jn+iXh3jvEAuU5sjjlEemeaIY9SLTHPEMdqPTHPEMfqB5HWM/iS9OsZ5Ift1TPI0RxyTXpojjsl+miOOyQ80RxyTP2mOOKYx0X7d98LTl90fPa+9+z5dVLhujfrNMFfG7xWdDPaPx6uo8joZ6o/cINOvjFPhxlGvU/9Ge5TrRZ2MMo5U5TX2SFVec19SldfJKP6RGj9LdV7UdTVhvmSK+ZIp5kummC+ZYr5kivmSKeZLppgvmWK+ZIr5kinmS6adrwvxO70h8H6RuE5cG/0e7zoxXMwVc6Lf480VI6NKIPyW4QZxmbCEAe0YeL9cuMKOfo/nivEiFF70LUUoJkS/38NPJeaLyUKKG6GdBu9XikWiGP0eb5GYLpaIhdDOhPdZ0e/3sHJpmbhGfEQsh3YovGMVUye8rocW65Q64WVCi7+764x+d9cZ/e6uM/rdXWf0u7vO6Hd3ndHv7jrh9WFon1v2banU/rCcprYoTY0SjRnXE2lZqQNiOU1tUZoaJRpT1dvIKWqLKpoapYquRkmp5ZEpZWSG2qKKpkapVR1TMamOSWeP7vu4ofC8VWv3xsCTgvVHw+E1rqH+aAg8g5dGlXxf3nlSKnU0idw9s8pxbQXL31rzHanU+LD84tPV2uS41oNlsi2uGWH5wMIXpVK7xPLBA8elUgPF8punXpBKLRXLJ2a8IJWaLJZJPq6tYJn0xjUaLJP9ca0Hy+SHuGaEZfJnXHvCMs1LXMPCMs1vXAvDMsaJUlPDMsortTkso16lxodltF+pFWIZ/aDUHLGM/lRql1jGeVFqoFjG+VVqqVjGOFFqslgmeYoZjkkvxQzHZD/FDMfkB4oZjsmfFDMc07xQzHBM80sxwzHpHfw95+DvOQd/zzn4e84P4u85cY1S6jgSeeiS70ulNoTl5/d+Tyo1Jiw/ddsrUqlVYZlsi2sWWP7a/hNSqZ1h+YlNx6RSg8Py0i8dlUotD8tvPPO8VGqCWCb5+Lf9LJPeuEaAZbI/rjVgmfwQ1yywTP6Max9YpnmJayhYpvmNazFYxjhRajpYRnmlNoRl1KvUmLCM9iu1KiyjH5SaF5bRn0rtDMs4L0oNDss4v0otD8sYJ0pNEMskTzHDMemlmOGY7KeY4Zj8QDHDMfmTYoZjmheKGY5pfilmOCa9g+elwfPS4Hlp8Lz0QTwv3dvxolTqWVh+9cxbiUzycf0IyyTfilFeqWdhGeWTmOTVMRuZ5FvxYP1L6/qX4yPPzFfqUFh++vShDqWeheX1r12zQKlDYXncE7MWKPUsLKNepQ6FZdSr1LOwjHqVOhSWUa9Sz8KyppZEre/Q1aTIlDKSq1tRr6t6NbUknD0yhT0yhT2ylT36z8mxbmVo9P9eV1+3gp+Tj4TXhLrPyV+auq9DqUNh+YGpRzuUehaWza8fk0odCsvuS0elUs/CMupV6lBYRr1KPQvLqFepQ2EZ9Sr1LCxragHU3+fragpkShnJ1R2o11W9mloAzh6Zwh6Zwh7Zyh6cF6UOhWWcF6WehWWcF6UOhWWcF6WeheVqnNTqUFiuxkmtnoXlapzU6lBYrsZJrZ6F5cH4aR0/8Nx3KLUqLI+5/EiHUlfCMsor9SksP7r/1x1KzQvLczZ8Uyo1KYm8cuyzUqkTSWTsq9SkJPLwI0elUvOSyHi/Sn2KVOpTahzXWUR1HHGNBtWqVBrqStQ6kaguo0Gm2FAbkiRTbKgfobqYYkNdDNVxyIY6FLWmpqWMao9qg66vTj6Nbeq96GSGwA49Hvbd8bBP4748GdrJsDNfDLv3FGinRPWkAvbzUfCaKq6CfXwotFjtfBXs1SOhHQrvM2BfHxdVnkwEniSmRf9/taOF//5nO6jeRMfri4uLVG+i47t+9HiR6k10vK88t0j1JjpGvVRvomPUS/UmOka9VG+iY9RL9SY6Hvwdb+vf8b7/8rNFqjfR8RffeqdI9SY6/uVnLpdUb6Jj69zPilRvomPUS/UmOka9VG+iY9RL9SY6Rr1Ub6LjwfhpHT/BH6ZJqjfR8cWjb5RUb6Ljp7+yTlK9iY5/+HlXUr2JjlEv1ZvoGPVSvYmOUS/Vm+gY9VK9iY4H46d1/JybVpJUb6Ljtyc+JKneRMff+PljkupNdPzICw9KqjfRMeqlehMdo16qN9Ex6qV6Ex2jXqo30fFg/CTWoSxQ6jIS+VP3VDmuHWD58KGJC5SaEZZJb1zLwPKcDVcsUGpYWF6yf/wCpRaG5Xs7xi9QampYJvm4doBl0hvXILBM9se1DCyTH+KaCJbJn3FtBcs4L0qNBssor9R6sIx6lZoRltF+pfaEZfSDUsPCMvpTqYVhGedFqalhmeRpjjgmvTRHHJP9NEcckx9ojjgmf9IccUxjDtahDNahDNah/P/Uofwv8t+0JQ=='}, 'lowergate': {'bytes': 45236, 'sha256': 'fd92505c11a7de3706cc854d8971e260b7ee6425c5b6a835a50cfac282c680cb', 'compressed': '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'}}
SOURCE_INPUTS = {'uppergate': {'bytes': 11987, 'sha256': 'c18a41bc3f3bb659abbb7a1ff0642867cd99bed4c317ea2d555e804073770845', 'compressed': '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'}, 'lowergate': {'bytes': 11987, 'sha256': 'c18a41bc3f3bb659abbb7a1ff0642867cd99bed4c317ea2d555e804073770845', 'compressed': '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'}}
PALETTE = [('SceneOnlyFoundation', (0.25, 0.28, 0.27, 1), 0.93), ('SceneOnlyBankStone', (0.43, 0.43, 0.37, 1), 0.9), ('SceneOnlyStaticWaterAppearance', (0.055, 0.23, 0.26, 1), 0.42)]
G = {}

def record(name, v, fs, m):
    ts = []
    mats = []
    for i, f in enumerate(fs):
        for k in range(1, len(f) - 1):
            ts.append((f[0], f[k], f[k + 1]))
            mats.append(m[i] if isinstance(m, list) else m)
    vol = sum((sum((v[a][i] * [v[b][1] * v[c][2] - v[b][2] * v[c][1], v[b][2] * v[c][0] - v[b][0] * v[c][2], v[b][0] * v[c][1] - v[b][1] * v[c][0]][i] for i in range(3))) for a, b, c in ts)) / 6
    if vol < 0:
        ts = [(a, c, b) for a, b, c in ts]
    assert abs(vol) > 1e-12
    G[name] = (v, ts, mats)

def rect(x, y0, y1, r):
    return [(-x + r, y0), (x - r, y0), (x, y0 + r), (x, y1 - r), (x - r, y1), (-x + r, y1), (-x, y1 - r), (-x, y0 + r)]

def prism(name, p, z0, z1, m, transform=None):
    v = [(x, y, z) for z in [z0, z1] for x, y in p]
    n = len(p)
    f = [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
    if transform:
        v = [transform(q) for q in v]
    record(name, v, f, m)

def box(name, lo, hi, m, transform=None):
    prism(name, [(lo[0], lo[1]), (hi[0], lo[1]), (hi[0], hi[1]), (lo[0], hi[1])], lo[2], hi[2], m, transform)

def union_boxes(name, boxes, m):
    xs = sorted(set((p[0] for b in boxes for p in b)))
    ys = sorted(set((p[1] for b in boxes for p in b)))
    zs = sorted(set((p[2] for b in boxes for p in b)))
    faces = {}
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            for k in range(len(zs) - 1):
                c = ((xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2, (zs[k] + zs[k + 1]) / 2)
                if not any((all((lo[t] < c[t] < hi[t] for t in range(3))) for lo, hi in boxes)):
                    continue
                v = [(x, y, z) for z in [zs[k], zs[k + 1]] for y in [ys[j], ys[j + 1]] for x in [xs[i], xs[i + 1]]]
                for f in [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]:
                    q = tuple((v[t] for t in f))
                    key = tuple(sorted(q))
                    if key in faces:
                        del faces[key]
                    else:
                        faces[key] = q
    verts = []
    ix = {}
    fs = []
    for q in faces.values():
        f = []
        for p in q:
            if p not in ix:
                ix[p] = len(verts)
                verts.append(p)
            f.append(ix[p])
        fs.append(f)
    record(name, verts, fs, m)

def cyl(name, center, r, length, axis, m, n=12):
    axes = [i for i in range(3) if i != axis]
    v = []
    for end in [-0.5, 0.5]:
        for i in range(n):
            p = list(center)
            p[axis] += end * length
            p[axes[0]] += r * math.cos(i * math.tau / n)
            p[axes[1]] += r * math.sin(i * math.tau / n)
            v.append(tuple(p))
    record(name, v, [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)], m)

def sweep(name, path, r, m, n=12):
    v = []
    for j, p in enumerate(path):
        a = path[max(0, j - 1)]
        b = path[min(len(path) - 1, j + 1)]
        dy = b[1] - a[1]
        dz = b[2] - a[2]
        q = math.hypot(dy, dz)
        u = (0, dz / q, -dy / q)
        for i in range(n):
            t = math.tau * i / n
            v.append((p[0] + r * math.cos(t), p[1] + u[1] * r * math.sin(t), p[2] + u[2] * r * math.sin(t)))
    fs = [tuple(reversed(range(n))), tuple(((len(path) - 1) * n + i for i in range(n)))]
    fs += [(k * n + i, k * n + (i + 1) % n, (k + 1) * n + (i + 1) % n, (k + 1) * n + i) for k in range(len(path) - 1) for i in range(n)]
    record(name, v, fs, m)

def ring(name, x0, x1, y, th, z0, z1, m, tr=None):
    outer = [(x0, -y), (x1, -y), (x1, y), (x0, y)]
    inner = [(x0 + th, -y + th), (x1 - th, -y + th), (x1 - th, y - th), (x0 + th, y - th)]
    v = [(x, y, z) for z, p in [(z0, outer), (z0, inner), (z1, outer), (z1, inner)] for x, y in p]
    fs = []
    for i in range(4):
        j = (i + 1) % 4
        fs += [(i, j, 4 + j, 4 + i), (8 + i, 12 + i, 12 + j, 8 + j), (i, 8 + i, 8 + j, j), (4 + i, 4 + j, 12 + j, 12 + i)]
    if tr:
        v = [tr(p) for p in v]
    record(name, v, fs, m)

def rod(name, a, b, r, m, n=8):
    d = [b[i] - a[i] for i in range(3)]
    le = math.sqrt(sum((t * t for t in d)))
    w = [t / le for t in d]
    seed = [0, 0, 1] if abs(w[2]) < 0.9 else [0, 1, 0]
    u = [w[1] * seed[2] - w[2] * seed[1], w[2] * seed[0] - w[0] * seed[2], w[0] * seed[1] - w[1] * seed[0]]
    le = math.sqrt(sum((t * t for t in u)))
    u = [t / le for t in u]
    v = [w[1] * u[2] - w[2] * u[1], w[2] * u[0] - w[0] * u[2], w[0] * u[1] - w[1] * u[0]]
    vs = [tuple((p[k] + r * (u[k] * math.cos(math.tau * i / n) + v[k] * math.sin(math.tau * i / n)) for k in range(3))) for p in [a, b] for i in range(n)]
    record(name, vs, [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)], m)

def earclip(poly):
    ids = list(range(len(poly)))
    out = []

    def cross2(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    while len(ids) > 3:
        done = False
        for k, i in enumerate(ids):
            a, b, c = (ids[k - 1], i, ids[(k + 1) % len(ids)])
            if cross2(poly[a], poly[b], poly[c]) <= 1e-13:
                continue
            if any((j not in [a, b, c] and min(cross2(poly[a], poly[b], poly[j]), cross2(poly[b], poly[c], poly[j]), cross2(poly[c], poly[a], poly[j])) >= -1e-13 for j in ids)):
                continue
            out.append((a, b, c))
            ids.pop(k)
            done = True
            break
        assert done, 'Cannot triangulate complete outer shell'
    out.append(tuple(ids))
    return out

def annular_x(name, x, z, ri, ro, th, m, n=32):
    vs = [(xx, r * math.cos(i * math.tau / n), z + r * math.sin(i * math.tau / n)) for xx, r in [(x - th / 2, ri), (x - th / 2, ro), (x + th / 2, ro), (x + th / 2, ri)] for i in range(n)]
    fs = [(j * n + i, j * n + (i + 1) % n, (j + 1) % 4 * n + (i + 1) % n, (j + 1) % 4 * n + i) for j in range(4) for i in range(n)]
    record(name, vs, fs, m)

def axial_profile(name, profile, center, axis, m, n=32):
    axes = [i for i in range(3) if i != axis]
    vs = []
    rings = []
    for r, z in profile:
        row = []
        for j in range(1 if r == 0 else n):
            p = list(center)
            p[axis] += z
            p[axes[0]] += r * math.cos(j * math.tau / n)
            p[axes[1]] += r * math.sin(j * math.tau / n)
            row.append(len(vs))
            vs.append(tuple(p))
        rings.append(row)
    fs = []
    for k, row in enumerate(rings):
        nex = rings[(k + 1) % len(rings)]
        if len(row) == len(nex) == 1:
            continue
        for j in range(n):
            jj = (j + 1) % n
            if len(row) == 1:
                fs.append((row[0], nex[j], nex[jj]))
            elif len(nex) == 1:
                fs.append((row[j], nex[0], row[jj]))
            else:
                fs.append((row[j], nex[j], nex[jj], row[jj]))
    record(name, vs, fs, m)

def make_geometry():
    G.clear()
    box('SceneOnlyCanalLockFloor', (-3.1, -5.7, 0), (3.1, 5.7, 0.12), 0)
    b = [((-3.1, -5.7, 0.1), (-1.85, 5.7, 1.5)), ((1.85, -5.7, 0.1), (3.1, 5.7, 1.5))]
    for ya, yb in [(-5.7, -4.5), (-2.0, 2.0), (4.5, 5.7)]:
        b.extend([((-1.5, ya, 0.1), (1.5, yb, 0.27)), ((-1.85, ya, 0.1), (-1.5, yb, 1.72)), ((1.5, ya, 0.1), (1.85, yb, 1.72))])
    union_boxes('SceneOnlyCanalLockContinuousBanksAndBed', b, 1)
    w = 1.48
    slope = 0.57 / 1.51

    def back(y, x):
        return y - 0.11 + slope * abs(x) + 0.012

    def front(y, x):
        return y - 0.29 + slope * abs(x) - 0.1
    prism('SceneOnlyCanalLockUpperWater', [(-w, back(3.25, w)), (0, back(3.25, 0)), (w, back(3.25, w)), (w, 5.69), (-w, 5.69)], 0.27, 1.22, 2)
    prism('SceneOnlyCanalLockMiddleWater', [(-w, back(-3.25, w)), (0, back(-3.25, 0)), (w, back(-3.25, w)), (w, front(3.25, w)), (0, front(3.25, 0)), (-w, front(3.25, w))], 0.27, 0.7, 2)
    prism('SceneOnlyCanalLockLowerWater', [(-w, -5.69), (w, -5.69), (w, front(-3.25, w)), (0, front(-3.25, 0)), (-w, front(-3.25, w))], 0.27, 0.43, 2)
    return G

def pack_glb(doc, blob):
    j = json.dumps(doc, separators=(',', ':'), allow_nan=False).encode()
    j += b' ' * (-len(j) % 4)
    b = bytes(blob) + b'\x00' * (-len(blob) % 4)
    return struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(j) + 8 + len(b)) + struct.pack('<II', len(j), 1313821514) + j + struct.pack('<II', len(b), 5130562) + b

def compose_floor(inputs):
    make_geometry()
    d = dict(asset={'version': '2.0', 'generator': 'Original static mesh construction'}, scene=0, scenes=[{'name': TITLE, 'nodes': [0]}], nodes=[{'name': 'AssetRoot__' + ASSET, 'children': []}], meshes=[], materials=[{'name': n, 'doubleSided': True, 'pbrMetallicRoughness': {'baseColorFactor': c, 'metallicFactor': 0.0, 'roughnessFactor': r}} for n, c, r in PALETTE], accessors=[], bufferViews=[], buffers=[])
    blob = bytearray()

    def array(values, component, kind):
        flat = [v for row in values for v in row] if kind == 'VEC3' else values
        fmt = 'f' if component == 5126 else 'I'
        raw = struct.pack('<' + fmt * len(flat), *flat)
        offset = len(blob)
        blob.extend(raw)
        blob.extend(b'\x00' * (-len(blob) % 4))
        view = len(d['bufferViews'])
        d['bufferViews'].append({'buffer': 0, 'byteOffset': offset, 'byteLength': len(raw)})
        a = {'bufferView': view, 'componentType': component, 'count': len(values), 'type': kind}
        if kind == 'VEC3':
            a.update(min=[min((p[k] for p in values)) for k in range(3)], max=[max((p[k] for p in values)) for k in range(3)])
        index = len(d['accessors'])
        d['accessors'].append(a)
        return index
    for name, (v, fs, mats) in G.items():
        prim = []
        for mat in sorted(set(mats)):
            positions = []
            normals = []
            for ids, mi in zip(fs, mats):
                if mi != mat:
                    continue
                a, b, c = [v[i] for i in ids]
                u = [b[k] - a[k] for k in range(3)]
                w = [c[k] - a[k] for k in range(3)]
                n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
                le = math.sqrt(sum((x * x for x in n)))
                assert le > 1e-12
                n = [x / le for x in n]
                positions.extend(((x, z, -y) for x, y, z in [a, b, c]))
                normals.extend([(n[0], n[2], -n[1])] * 3)
            prim.append({'attributes': {'POSITION': array(positions, 5126, 'VEC3'), 'NORMAL': array(normals, 5126, 'VEC3')}, 'indices': array(list(range(len(positions))), 5125, 'SCALAR'), 'material': mat, 'mode': 4})
        mesh = len(d['meshes'])
        d['meshes'].append({'name': name, 'primitives': prim})
        node = len(d['nodes'])
        d['nodes'].append({'name': name, 'mesh': mesh})
        d['nodes'][0]['children'].append(node)
    d['buffers'] = [{'byteLength': len(blob)}]
    return (d, bytes(blob), {'new_original_geometry': True, 'triangles': sum((len(f) for v, f, m in G.values())), 'mesh_count': len(G), 'whole_original_model_count': 0, 'static_pose_only': True})
PLACEMENTS = [('uppergate', (0.0, 3.25, 0.12)), ('lowergate', (0.0, -3.25, 0.12))]

def decode_document(raw):
    assert raw[:4] == b'glTF'
    p = 12
    d = None
    b = None
    while p < len(raw):
        n, k = struct.unpack_from('<II', raw, p)
        chunk = raw[p + 8:p + 8 + n]
        p += 8 + n
        if k == 1313821514:
            d = json.loads(chunk)
        elif k == 5130562:
            b = chunk
    assert d is not None and b is not None
    return (d, b)

def compose(inputs):
    d = dict(asset={'version': '2.0', 'generator': 'Complete original GLB payloads with rigid whole-instance parent wrappers'}, scene=0, scenes=[{'name': TITLE, 'nodes': [0]}], nodes=[{'name': 'WholeCanalLockScene', 'children': []}], materials=[], meshes=[], accessors=[], bufferViews=[], buffers=[])
    blob = bytearray()

    def append(doc, data, label, t):
        assert len(doc['buffers']) == 1 and (not any((doc.get(x) for x in ['skins', 'animations', 'textures', 'images'])))
        assert len(data) >= doc['buffers'][0]['byteLength']
        no, mo, ma, ac, bv = (len(d['nodes']), len(d['meshes']), len(d['materials']), len(d['accessors']), len(d['bufferViews']))
        offset = len(blob)
        blob.extend(data[:doc['buffers'][0]['byteLength']])
        blob.extend(b'\x00' * (-len(blob) % 4))
        d['materials'].extend(copy.deepcopy(doc['materials']))
        for v in doc['bufferViews']:
            v = copy.deepcopy(v)
            assert v.get('buffer', 0) == 0
            v['buffer'] = 0
            v['byteOffset'] = v.get('byteOffset', 0) + offset
            d['bufferViews'].append(v)
        for v in doc['accessors']:
            v = copy.deepcopy(v)
            assert 'sparse' not in v
            v['bufferView'] += bv
            d['accessors'].append(v)
        for m in doc['meshes']:
            m = copy.deepcopy(m)
            for p in m['primitives']:
                assert not p.get('targets')
                p['attributes'] = {k: v + ac for k, v in p['attributes'].items()}
                p['indices'] += ac
                p['material'] += ma
            d['meshes'].append(m)
        for n in doc['nodes']:
            n = copy.deepcopy(n)
            if label != 'SceneOnlyCanalLockGeometry':
                n.setdefault('extras', {})['whole_original_node_name'] = n.get('name', '')
                n['name'] = label + '__' + n.get('name', '')
            if 'mesh' in n:
                n['mesh'] += mo
            if 'children' in n:
                n['children'] = [i + no for i in n['children']]
            d['nodes'].append(n)
        root = len(d['nodes'])
        d['nodes'].append(dict(name='WholeInstance_' + label, translation=[t[0], t[2], -t[1]], children=[no + i for i in doc['scenes'][doc.get('scene', 0)]['nodes']], extras={'unit_scale': True, 'whole_original_payload': True, 'translation_only_wrapper': True}))
        d['nodes'][0]['children'].append(root)
    for label, t in PLACEMENTS:
        v = INPUTS[label]
        raw = zlib.decompress(base64.b64decode(v['compressed']))
        assert len(raw) == v['bytes'] and hashlib.sha256(raw).hexdigest() == v['sha256']
        doc, data = decode_document(raw)
        append(doc, data, label, t)
    floor, data, proof = compose_floor({})
    append(floor, data, 'SceneOnlyCanalLockGeometry', (0, 0, 0))
    d['buffers'] = [{'byteLength': len(blob)}]
    return (d, bytes(blob), dict(new_original_geometry=False, triangles=1620, mesh_count=59, whole_original_model_count=0, scene_count=1, complete_existing_instances=2, static_pose_only=True, original_payloads={k: {a: v[a] for a in ['bytes', 'sha256']} for k, v in INPUTS.items()}, rigid_placements=PLACEMENTS, quarterturn_z_labels=[]))

def main():
    import bpy, sys, time
    from mathutils import Vector
    OUT = Path(__file__).resolve().parent
    inputs = {k: zlib.decompress(base64.b64decode(v['compressed'])) for k, v in INPUTS.items()}
    for k, raw in inputs.items():
        assert hashlib.sha256(raw).hexdigest() == INPUTS[k]['sha256']
    for v in SOURCE_INPUTS.values():
        assert hashlib.sha256(zlib.decompress(base64.b64decode(v['compressed']))).hexdigest() == v['sha256']
    document, blob, proof = compose(inputs)
    model = pack_glb(document, blob)
    (OUT / 'model.glb').write_bytes(model)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(OUT / 'model.glb'))
    parts = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    assert len(parts) == 59
    triangle_count = sum((len(p.vertices) - 2 for o in parts for p in o.data.polygons))
    assert triangle_count == proof['triangles']
    points = [o.matrix_world @ v.co for o in parts for v in o.data.vertices]
    lo = [min((v[k] for v in points)) for k in range(3)]
    hi = [max((v[k] for v in points)) for k in range(3)]
    assert abs(lo[2]) <= TOL and abs(lo[0] + hi[0]) <= TOL and (abs(lo[1] + hi[1]) <= TOL)
    assert len({m for o in parts for m in o.data.materials}) == 9
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.use_denoising = False
    for layer in scene.view_layers:
        layer.cycles.use_denoising = False
    scene.use_nodes = False
    scene.render.use_compositing = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.render.resolution_x = scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.world = scene.world or bpy.data.worlds.new('Neutral instrument preview')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.3, 0.3, 0.3, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.8
    scene.view_settings.view_transform = 'AgX'
    focus = Vector((0.0, 0.0, 0.8))

    def aim(o, pos):
        o.location = pos
        o.rotation_euler = (focus - o.location).to_track_quat('-Z', 'Y').to_euler()
    for name, pos, power, size in [('Key', (-12, -15, 20), 3200, 12), ('Fill', (14, -9, 15), 2200, 10), ('Rim', (6, 15, 18), 2800, 10)]:
        bpy.ops.object.light_add(type='AREA', location=pos)
        o = bpy.context.object
        o.name = 'Preview_' + name
        o.data.energy = power
        o.data.shape = 'DISK'
        o.data.size = size
        aim(o, pos)
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.name = 'Preview_Camera'
    cam.data.type = 'ORTHO'
    scene.camera = cam
    aim(cam, (10, -14, 13))
    bpy.context.view_layer.update()
    rot = cam.rotation_euler.to_quaternion()
    right = rot @ Vector((1, 0, 0))
    up = rot @ Vector((0, 1, 0))
    xx = [v.dot(right) for v in points]
    yy = [v.dot(up) for v in points]
    cam.location += right * ((min(xx) + max(xx)) / 2 - cam.location.dot(right)) + up * ((min(yy) + max(yy)) / 2 - cam.location.dot(up))
    cam.data.ortho_scale = max(max(xx) - min(xx), max(yy) - min(yy)) * 1.12
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.0003))
    ground = bpy.context.object
    ground.name = 'Preview_ground_not_asset'
    mat = bpy.data.materials.new('Preview_slate')
    mat.diffuse_color = (0.2, 0.24, 0.25, 1)
    ground.data.materials.append(mat)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'source.blend'), compress=False)

    def config():
        return dict(engine=scene.render.engine, samples=scene.cycles.samples, adaptive=scene.cycles.use_adaptive_sampling, cycles_denoise=scene.cycles.use_denoising, view_layer_denoise=[x.cycles.use_denoising for x in scene.view_layers], compositor_nodes=scene.use_nodes, compositing=scene.render.use_compositing, threads_mode=scene.render.threads_mode, threads=scene.render.threads)
    qa = {'review_mode': 'SELF_REVIEW', 'status': 'GEOMETRY_CREATED_NEEDS_MAKER_REVIEW', 'asset_id': ASSET, 'asset': ASSET, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'glb_sha256': hashlib.sha256(model).hexdigest(), 'mesh_count': 59, 'mesh_objects': 59, 'triangles': triangle_count, 'materials': 9, 'bounds_min_m': lo, 'bounds_max_m': hi, 'composition': proof, 'native_readback_claim': False, 'normal_setter_or_vertex_bake_used': False, 'render_configuration': {'samples': 128, 'threads': 4, 'engine': 'CYCLES', 'denoising': False}}
    qa['native_saved_render_config'] = config()
    qa['render_configs'] = {}
    if '--geometry-only' not in sys.argv:
        view = sys.argv[sys.argv.index('--tier-single-view') + 1] if '--tier-single-view' in sys.argv else 'thumbnail'
        assert view in ['qa-front', 'thumbnail']
        scene.cycles.samples = 16 if view == 'qa-front' else 128
        qa['render_configs'][view] = config()
        scene.render.filepath = str(OUT / (view + '.png'))
        start = time.monotonic()
        bpy.ops.render.render(write_still=True)
        qa['render'] = {'view': view, 'samples': scene.cycles.samples, 'seconds': time.monotonic() - start, 'original_pixels_reviewed': False}
    (OUT / 'qa-report.json').write_text(json.dumps(qa, indent=2) + '\n')
    files = {}
    for role, name in [('glb', 'model.glb'), ('blend', 'source.blend'), ('generator', 'generate.py'), ('render', 'thumbnail.png')]:
        p = OUT / name
        if p.exists():
            files[role] = {'path': f'assets/waterworks/{ASSET}/v1.0.0/{name}', 'size': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    if len(files) == 4:
        meta = {'id': ASSET, 'version': '1.0.0', 'category': 'scenes', 'assetKind': 'scene', 'theme': 'waterworks', 'style': 'source-preserved-low-poly', 'title': TITLE, 'description': 'One static canal-lock exterior scene and zero new independent models. Two complete qualified balanced twin mitre gate modules retain every original mesh, raw GLB buffer, material dictionary and internal node hierarchy at original unit scale, with only separate longitudinal translation wrappers. New scene-only geometry joins their short mouths into a long narrow chamber between continuous outer banks, with a grounded slab and three separate opaque water-appearance volumes at distinct fixed levels. The upstream approach, enclosed middle chamber and downstream approach are visibly divided by the two intact angled gate pairs; original balance beams and pivot fittings remain intact above the banks. This is not a second gate counted as a new model: the scene relation is a long intervening chamber and two external approaches on a connected bank-and-bed layout, unlike the old single dry sluice/wheel race equipment scene. Water appearance deliberately stops short of reinforcing rails and leaves small wall clearances; it is not a sealed fluid simulation. No gates are cut, pivoted, scaled, recoloured, or extracted from their original mouth modules. No hydraulic operation, filling, flow, navigation, boat clearance, gate compatibility, watertightness, walkway access, load, engineering, installation or safety capability. Rigging, animation and interaction not made or verified.', 'bounds': dict(zip(['x', 'y', 'z'], [hi[k] - lo[k] for k in range(3)]), unit='m'), 'triangles': triangle_count, 'materials': 9, 'files': files, 'status': 'review', 'license': 'All rights reserved'}
        (OUT / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
    print('SCENE_STAGE_COMPLETE', ASSET, triangle_count)
if __name__ == '__main__':
    main()
