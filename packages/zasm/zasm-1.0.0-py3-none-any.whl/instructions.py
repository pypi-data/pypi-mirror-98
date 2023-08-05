import re
from defs import *
# Instructions text listed below is a modified version of
# a file taken from:  https://github.com/toptensoftware/yazd

db = '''
CE ::            ADC A,::
8E               ADC A,(HL)
DD 8E ::         ADC A,(IX+::)
FD 8E ::         ADC A,(IY+::)
8F               ADC A,A
88               ADC A,B
89               ADC A,C
8A               ADC A,D
8B               ADC A,E
8C               ADC A,H
DD 8C            ADC A,IXH
DD 8D            ADC A,IXL
FD 8C            ADC A,IYH
FD 8D            ADC A,IYL
8D               ADC A,L
ED 4A            ADC HL,BC
ED 5A            ADC HL,DE
ED 6A            ADC HL,HL
ED 7A            ADC HL,SP
C6 ::            ADD A,::
86               ADD A,(HL)
DD 86 ::         ADD A,(IX+::)
FD 86 ::         ADD A,(IY+::)
87               ADD A,A
80               ADD A,B
81               ADD A,C
82               ADD A,D
83               ADD A,E
84               ADD A,H
DD 84            ADD A,IXH
DD 85            ADD A,IXL
FD 84            ADD A,IYH
FD 85            ADD A,IYL
85               ADD A,L
09               ADD HL,BC
19               ADD HL,DE
29               ADD HL,HL
39               ADD HL,SP
DD 09            ADD IX,BC
DD 19            ADD IX,DE
DD 29            ADD IX,IX
DD 39            ADD IX,SP
FD 09            ADD IY,BC
FD 19            ADD IY,DE
FD 29            ADD IY,IY
FD 39            ADD IY,SP
E6 ::            AND ::
A6               AND (HL)
DD A6 ::         AND (IX+::)
FD A6 ::         AND (IY+::)
A7               AND A
A6               AND A,(HL)
A7               AND A,A
A0               AND A,B
A1               AND A,C
A2               AND A,D
A3               AND A,E
A4               AND A,H
A5               AND A,L
A0               AND B
A1               AND C
A2               AND D
A3               AND E
A4               AND H
DD A4            AND IXH
DD A5            AND IXL
FD A4            AND IYH
FD A5            AND IYL
A5               AND L
CB 46            BIT 0,(HL)
CB 4E            BIT 1,(HL)
CB 56            BIT 2,(HL)
CB 5E            BIT 3,(HL)
CB 66            BIT 4,(HL)
CB 6E            BIT 5,(HL)
CB 76            BIT 6,(HL)
CB 7E            BIT 7,(HL)
DD CB :: 46      BIT 0,(IX+::)
DD CB :: 4E      BIT 1,(IX+::)
DD CB :: 56      BIT 2,(IX+::)
DD CB :: 5E      BIT 3,(IX+::)
DD CB :: 66      BIT 4,(IX+::)
DD CB :: 6E      BIT 5,(IX+::)
DD CB :: 76      BIT 6,(IX+::)
DD CB :: 7E      BIT 7,(IX+::)
FD CB :: 40      BIT 0,(IY+::)
FD CB :: 48      BIT 1,(IY+::)
FD CB :: 50      BIT 2,(IY+::)
FD CB :: 58      BIT 3,(IY+::)
FD CB :: 60      BIT 4,(IY+::)
FD CB :: 68      BIT 5,(IY+::)
FD CB :: 70      BIT 6,(IY+::)
FD CB :: 78      BIT 7,(IY+::)
CB 47            BIT 0,A
CB 4F            BIT 1,A
CB 57            BIT 2,A
CB 5F            BIT 3,A
CB 67            BIT 4,A
CB 6F            BIT 5,A
CB 77            BIT 6,A
CB 7F            BIT 7,A
CB 40            BIT 0,B
CB 48            BIT 1,B
CB 50            BIT 2,B
CB 58            BIT 3,B
CB 60            BIT 4,B
CB 68            BIT 5,B
CB 70            BIT 6,B
CB 78            BIT 7,B
CB 41            BIT 0,C
CB 49            BIT 1,C
CB 51            BIT 2,C
CB 59            BIT 3,C
CB 61            BIT 4,C
CB 69            BIT 5,C
CB 71            BIT 6,C
CB 79            BIT 7,C
CB 42            BIT 0,D
CB 4A            BIT 1,D
CB 52            BIT 2,D
CB 5A            BIT 3,D
CB 62            BIT 4,D
CB 6A            BIT 5,D
CB 72            BIT 6,D
CB 7A            BIT 7,D
CB 43            BIT 0,E
CB 4B            BIT 1,E
CB 53            BIT 2,E
CB 5B            BIT 3,E
CB 63            BIT 4,E
CB 6B            BIT 5,E
CB 73            BIT 6,E
CB 7B            BIT 7,E
CB 44            BIT 0,H
CB 4C            BIT 1,H
CB 54            BIT 2,H
CB 5C            BIT 3,H
CB 64            BIT 4,H
CB 6C            BIT 5,H
CB 74            BIT 6,H
CB 7C            BIT 7,H
CB 45            BIT 0,L
CB 4D            BIT 1,L
CB 55            BIT 2,L
CB 5D            BIT 3,L
CB 65            BIT 4,L
CB 6D            BIT 5,L
CB 75            BIT 6,L
CB 7D            BIT 7,L
CD :: ::         CALL @@
DC :: ::         CALL C,@@
FC :: ::         CALL M,@@
D4 :: ::         CALL NC,@@
C4 :: ::         CALL NZ,@@
F4 :: ::         CALL P,@@
EC :: ::         CALL PE,@@
E4 :: ::         CALL PO,@@
CC :: ::         CALL Z,@@
3F               CCF
FE ::            CP ::
BE               CP (HL)
DD BE ::         CP (IX+::)
FD BE ::         CP (IY+::)
BF               CP A
BE               CP A,(HL)
BF               CP A,A
B8               CP A,B
B9               CP A,C
BA               CP A,D
BB               CP A,E
BC               CP A,H
BD               CP A,L
B8               CP B
B9               CP C
BA               CP D
BB               CP E
BC               CP H
DD BC            CP IXH
DD BD            CP IXL
FD BC            CP IYH
FD BD            CP IYL
BD               CP L
ED A9            CPD
ED B9            CPDR
ED A1            CPI
ED B1            CPIR
2F               CPL
27               DAA
35               DEC (HL)
DD 35 ::         DEC (IX+::)
FD 35 ::         DEC (IY+::)
3D               DEC A
05               DEC B
0B               DEC BC
0D               DEC C
15               DEC D
1B               DEC DE
1D               DEC E
25               DEC H
2B               DEC HL
DD 2B            DEC IX
DD 25            DEC IXH
DD 2D            DEC IXL
FD 2B            DEC IY
FD 25            DEC IYH
FD 2D            DEC IYL
2D               DEC L
3B               DEC SP
F3               DI
10 ::            DJNZ %%
FB               EI
E3               EX (SP),HL
DD E3            EX (SP),IX
FD E3            EX (SP),IY
08               EX AF,AF'
EB               EX DE,HL
D9               EXX
76               HALT
ED 46            IM 0
ED 56            IM 1
ED 5E            IM 2
DB ::            IN A,(::)
ED 78            IN A,(C)
ED 40            IN B,(C)
ED 48            IN C,(C)
ED 50            IN D,(C)
ED 58            IN E,(C)
ED 60            IN H,(C)
ED 68            IN L,(C)
ED 70            IN F,(C)
34               INC (HL)
DD 34 ::         INC (IX+::)
FD 34 ::         INC (IY+::)
3C               INC A
04               INC B
03               INC BC
0C               INC C
14               INC D
13               INC DE
1C               INC E
24               INC H
23               INC HL
DD 23            INC IX
DD 24            INC IXH
DD 2C            INC IXL
FD 23            INC IY
FD 24            INC IYH
FD 2C            INC IYL
2C               INC L
33               INC SP
ED AA            IND
ED BA            INDR
ED A2            INI
ED B2            INIR
E9               JP (HL)
DD E9            JP (IX)
FD E9            JP (IY)
C3 :: ::         JP @@
DA :: ::         JP C,@@
FA :: ::         JP M,@@
D2 :: ::         JP NC,@@
C2 :: ::         JP NZ,@@
F2 :: ::         JP P,@@
EA :: ::         JP PE,@@
E2 :: ::         JP PO,@@
CA :: ::         JP Z,@@
18 ::            JR %%
38 ::            JR C,%%
30 ::            JR NC,%%
20 ::            JR NZ,%%
28 ::            JR Z,%%
32 :: ::         LD (@@),A
ED 43 :: ::      LD (@@),BC
ED 53 :: ::      LD (@@),DE
22 :: ::         LD (@@),HL
DD 22 :: ::      LD (@@),IX
FD 22 :: ::      LD (@@),IY
ED 73 :: ::      LD (@@),SP
02               LD (BC),A
12               LD (DE),A
36 ::            LD (HL),::
77               LD (HL),A
70               LD (HL),B
71               LD (HL),C
72               LD (HL),D
73               LD (HL),E
74               LD (HL),H
75               LD (HL),L
DD 36 :: ::      LD (IX+::),::
DD 77 ::         LD (IX+::),A
DD 70 ::         LD (IX+::),B
DD 71 ::         LD (IX+::),C
DD 72 ::         LD (IX+::),D
DD 73 ::         LD (IX+::),E
DD 74 ::         LD (IX+::),H
DD 75 ::         LD (IX+::),L
FD 36 :: ::      LD (IY+::),::
FD 77 ::         LD (IY+::),A
FD 70 ::         LD (IY+::),B
FD 71 ::         LD (IY+::),C
FD 72 ::         LD (IY+::),D
FD 73 ::         LD (IY+::),E
FD 74 ::         LD (IY+::),H
FD 75 ::         LD (IY+::),L
3E ::            LD A,::
3A :: ::         LD A,(@@)
0A               LD A,(BC)
1A               LD A,(DE)
7E               LD A,(HL)
DD 7E ::         LD A,(IX+::)
FD 7E ::         LD A,(IY+::)
7F               LD A,A
78               LD A,B
79               LD A,C
7A               LD A,D
7B               LD A,E
7C               LD A,H
ED 57            LD A,I
DD 7C            LD A,IXH
DD 7D            LD A,IXL
FD 7C            LD A,IYH
FD 7D            LD A,IYL
7D               LD A,L
ED 5F            LD A,R
DD CB :: 87      LD A,RES 0,(IX+::)
DD CB :: 8F      LD A,RES 1,(IX+::)
DD CB :: 97      LD A,RES 2,(IX+::)
DD CB :: 9F      LD A,RES 3,(IX+::)
DD CB :: A7      LD A,RES 4,(IX+::)
DD CB :: AF      LD A,RES 5,(IX+::)
DD CB :: B7      LD A,RES 6,(IX+::)
DD CB :: BF      LD A,RES 7,(IX+::)
FD CB :: 87      LD A,RES 0,(IY+::)
FD CB :: 8F      LD A,RES 1,(IY+::)
FD CB :: 97      LD A,RES 2,(IY+::)
FD CB :: 9F      LD A,RES 3,(IY+::)
FD CB :: A7      LD A,RES 4,(IY+::)
FD CB :: AF      LD A,RES 5,(IY+::)
FD CB :: B7      LD A,RES 6,(IY+::)
FD CB :: BF      LD A,RES 7,(IY+::)
DD CB :: 17      LD A,RL (IX+::)
FD CB :: 17      LD A,RL (IY+::)
DD CB :: 07      LD A,RLC (IX+::)
FD CB :: 07      LD A,RLC (IY+::)
DD CB :: 1F      LD A,RR (IX+::)
FD CB :: 1F      LD A,RR (IY+::)
DD CB :: 0F      LD A,RRC (IX+::)
FD CB :: 0F      LD A,RRC (IY+::)
DD CB :: C7      LD A,SET 0,(IX+::)
DD CB :: CF      LD A,SET 1,(IX+::)
DD CB :: D7      LD A,SET 2,(IX+::)
DD CB :: DF      LD A,SET 3,(IX+::)
DD CB :: E7      LD A,SET 4,(IX+::)
DD CB :: EF      LD A,SET 5,(IX+::)
DD CB :: F7      LD A,SET 6,(IX+::)
DD CB :: FF      LD A,SET 7,(IX+::)
FD CB :: C7      LD A,SET 0,(IY+::)
FD CB :: CF      LD A,SET 1,(IY+::)
FD CB :: D7      LD A,SET 2,(IY+::)
FD CB :: DF      LD A,SET 3,(IY+::)
FD CB :: E7      LD A,SET 4,(IY+::)
FD CB :: EF      LD A,SET 5,(IY+::)
FD CB :: F7      LD A,SET 6,(IY+::)
FD CB :: FF      LD A,SET 7,(IY+::)
DD CB :: 27      LD A,SLA (IX+::)
FD CB :: 27      LD A,SLA (IY+::)
DD CB :: 37      LD A,SLL (IX+::)
FD CB :: 37      LD A,SLL (IY+::)
DD CB :: 2F      LD A,SRA (IX+::)
FD CB :: 2F      LD A,SRA (IY+::)
DD CB :: 3F      LD A,SRL (IX+::)
FD CB :: 3F      LD A,SRL (IY+::)
06 ::            LD B,::
46               LD B,(HL)
DD 46 ::         LD B,(IX+::)
FD 46 ::         LD B,(IY+::)
47               LD B,A
40               LD B,B
41               LD B,C
42               LD B,D
43               LD B,E
44               LD B,H
DD 44            LD B,IXH
DD 45            LD B,IXL
FD 44            LD B,IYH
FD 45            LD B,IYL
45               LD B,L
DD CB :: 80      LD B,RES 0,(IX+::)
DD CB :: 88      LD B,RES 1,(IX+::)
DD CB :: 90      LD B,RES 2,(IX+::)
DD CB :: 98      LD B,RES 3,(IX+::)
DD CB :: A0      LD B,RES 4,(IX+::)
DD CB :: A8      LD B,RES 5,(IX+::)
DD CB :: B0      LD B,RES 6,(IX+::)
DD CB :: B8      LD B,RES 7,(IX+::)
FD CB :: 80      LD B,RES 0,(IY+::)
FD CB :: 88      LD B,RES 1,(IY+::)
FD CB :: 90      LD B,RES 2,(IY+::)
FD CB :: 98      LD B,RES 3,(IY+::)
FD CB :: A0      LD B,RES 4,(IY+::)
FD CB :: A8      LD B,RES 5,(IY+::)
FD CB :: B0      LD B,RES 6,(IY+::)
FD CB :: B8      LD B,RES 7,(IY+::)
DD CB :: 10      LD B,RL (IX+::)
FD CB :: 10      LD B,RL (IY+::)
DD CB :: 00      LD B,RLC (IX+::)
FD CB :: 00      LD B,RLC (IY+::)
DD CB :: 18      LD B,RR (IX+::)
FD CB :: 18      LD B,RR (IY+::)
DD CB :: 08      LD B,RRC (IX+::)
FD CB :: 08      LD B,RRC (IY+::)
DD CB :: C0      LD B,SET 0,(IX+::)
DD CB :: C8      LD B,SET 1,(IX+::)
DD CB :: D0      LD B,SET 2,(IX+::)
DD CB :: D8      LD B,SET 3,(IX+::)
DD CB :: E0      LD B,SET 4,(IX+::)
DD CB :: E8      LD B,SET 5,(IX+::)
DD CB :: F0      LD B,SET 6,(IX+::)
DD CB :: F8      LD B,SET 7,(IX+::)
FD CB :: C0      LD B,SET 0,(IY+::)
FD CB :: C8      LD B,SET 1,(IY+::)
FD CB :: D0      LD B,SET 2,(IY+::)
FD CB :: D8      LD B,SET 3,(IY+::)
FD CB :: E0      LD B,SET 4,(IY+::)
FD CB :: E8      LD B,SET 5,(IY+::)
FD CB :: F0      LD B,SET 6,(IY+::)
FD CB :: F8      LD B,SET 7,(IY+::)
DD CB :: 20      LD B,SLA (IX+::)
FD CB :: 20      LD B,SLA (IY+::)
DD CB :: 30      LD B,SLL (IX+::)
FD CB :: 30      LD B,SLL (IY+::)
DD CB :: 28      LD B,SRA (IX+::)
FD CB :: 28      LD B,SRA (IY+::)
DD CB :: 38      LD B,SRL (IX+::)
FD CB :: 38      LD B,SRL (IY+::)
ED 4B :: ::      LD BC,(@@)
01 :: ::         LD BC,@@
0E ::            LD C,::
4E               LD C,(HL)
DD 4E ::         LD C,(IX+::)
FD 4E ::         LD C,(IY+::)
4F               LD C,A
48               LD C,B
49               LD C,C
4A               LD C,D
4B               LD C,E
4C               LD C,H
DD 4C            LD C,IXH
DD 4D            LD C,IXL
FD 4C            LD C,IYH
FD 4D            LD C,IYL
4D               LD C,L
DD CB :: 81      LD C,RES 0,(IX+::)
DD CB :: 89      LD C,RES 1,(IX+::)
DD CB :: 91      LD C,RES 2,(IX+::)
DD CB :: 99      LD C,RES 3,(IX+::)
DD CB :: A1      LD C,RES 4,(IX+::)
DD CB :: A9      LD C,RES 5,(IX+::)
DD CB :: B1      LD C,RES 6,(IX+::)
DD CB :: B9      LD C,RES 7,(IX+::)
FD CB :: 81      LD C,RES 0,(IY+::)
FD CB :: 89      LD C,RES 1,(IY+::)
FD CB :: 91      LD C,RES 2,(IY+::)
FD CB :: 99      LD C,RES 3,(IY+::)
FD CB :: A1      LD C,RES 4,(IY+::)
FD CB :: A9      LD C,RES 5,(IY+::)
FD CB :: B1      LD C,RES 6,(IY+::)
FD CB :: B9      LD C,RES 7,(IY+::)
DD CB :: 11      LD C,RL (IX+::)
FD CB :: 11      LD C,RL (IY+::)
DD CB :: 01      LD C,RLC (IX+::)
FD CB :: 01      LD C,RLC (IY+::)
DD CB :: 19      LD C,RR (IX+::)
FD CB :: 19      LD C,RR (IY+::)
DD CB :: 09      LD C,RRC (IX+::)
FD CB :: 09      LD C,RRC (IY+::)
DD CB :: C1      LD C,SET 0,(IX+::)
DD CB :: C9      LD C,SET 1,(IX+::)
DD CB :: D1      LD C,SET 2,(IX+::)
DD CB :: D9      LD C,SET 3,(IX+::)
DD CB :: E1      LD C,SET 4,(IX+::)
DD CB :: E9      LD C,SET 5,(IX+::)
DD CB :: F1      LD C,SET 6,(IX+::)
DD CB :: F9      LD C,SET 7,(IX+::)
FD CB :: C1      LD C,SET 0,(IY+::)
FD CB :: C9      LD C,SET 1,(IY+::)
FD CB :: D1      LD C,SET 2,(IY+::)
FD CB :: D9      LD C,SET 3,(IY+::)
FD CB :: E1      LD C,SET 4,(IY+::)
FD CB :: E9      LD C,SET 5,(IY+::)
FD CB :: F1      LD C,SET 6,(IY+::)
FD CB :: F9      LD C,SET 7,(IY+::)
DD CB :: 21      LD C,SLA (IX+::)
FD CB :: 21      LD C,SLA (IY+::)
DD CB :: 31      LD C,SLL (IX+::)
FD CB :: 31      LD C,SLL (IY+::)
DD CB :: 29      LD C,SRA (IX+::)
FD CB :: 29      LD C,SRA (IY+::)
DD CB :: 39      LD C,SRL (IX+::)
FD CB :: 39      LD C,SRL (IY+::)
16 ::            LD D,::
56               LD D,(HL)
DD 56 ::         LD D,(IX+::)
FD 56 ::         LD D,(IY+::)
57               LD D,A
50               LD D,B
51               LD D,C
52               LD D,D
53               LD D,E
54               LD D,H
DD 54            LD D,IXH
DD 55            LD D,IXL
FD 54            LD D,IYH
FD 55            LD D,IYL
55               LD D,L
DD CB :: 82      LD D,RES 0,(IX+::)
DD CB :: 8A      LD D,RES 1,(IX+::)
DD CB :: 92      LD D,RES 2,(IX+::)
DD CB :: 9A      LD D,RES 3,(IX+::)
DD CB :: A2      LD D,RES 4,(IX+::)
DD CB :: AA      LD D,RES 5,(IX+::)
DD CB :: B2      LD D,RES 6,(IX+::)
DD CB :: BA      LD D,RES 7,(IX+::)
FD CB :: 82      LD D,RES 0,(IY+::)
FD CB :: 8A      LD D,RES 1,(IY+::)
FD CB :: 92      LD D,RES 2,(IY+::)
FD CB :: 9A      LD D,RES 3,(IY+::)
FD CB :: A2      LD D,RES 4,(IY+::)
FD CB :: AA      LD D,RES 5,(IY+::)
FD CB :: B2      LD D,RES 6,(IY+::)
FD CB :: BA      LD D,RES 7,(IY+::)
DD CB :: 12      LD D,RL (IX+::)
FD CB :: 12      LD D,RL (IY+::)
DD CB :: 02      LD D,RLC (IX+::)
FD CB :: 02      LD D,RLC (IY+::)
DD CB :: 1A      LD D,RR (IX+::)
FD CB :: 1A      LD D,RR (IY+::)
DD CB :: 0A      LD D,RRC (IX+::)
FD CB :: 0A      LD D,RRC (IY+::)
DD CB :: C2      LD D,SET 0,(IX+::)
DD CB :: CA      LD D,SET 1,(IX+::)
DD CB :: D2      LD D,SET 2,(IX+::)
DD CB :: DA      LD D,SET 3,(IX+::)
DD CB :: E2      LD D,SET 4,(IX+::)
DD CB :: EA      LD D,SET 5,(IX+::)
DD CB :: F2      LD D,SET 6,(IX+::)
DD CB :: FA      LD D,SET 7,(IX+::)
FD CB :: C2      LD D,SET 0,(IY+::)
FD CB :: CA      LD D,SET 1,(IY+::)
FD CB :: D2      LD D,SET 2,(IY+::)
FD CB :: DA      LD D,SET 3,(IY+::)
FD CB :: E2      LD D,SET 4,(IY+::)
FD CB :: EA      LD D,SET 5,(IY+::)
FD CB :: F2      LD D,SET 6,(IY+::)
FD CB :: FA      LD D,SET 7,(IY+::)
DD CB :: 22      LD D,SLA (IX+::)
FD CB :: 22      LD D,SLA (IY+::)
DD CB :: 32      LD D,SLL (IX+::)
FD CB :: 32      LD D,SLL (IY+::)
DD CB :: 2A      LD D,SRA (IX+::)
FD CB :: 2A      LD D,SRA (IY+::)
DD CB :: 3A      LD D,SRL (IX+::)
FD CB :: 3A      LD D,SRL (IY+::)
ED 5B :: ::      LD DE,(@@)
11 :: ::         LD DE,@@
1E ::            LD E,::
5E               LD E,(HL)
DD 5E ::         LD E,(IX+::)
FD 5E ::         LD E,(IY+::)
5F               LD E,A
58               LD E,B
59               LD E,C
5A               LD E,D
5B               LD E,E
5C               LD E,H
DD 5C            LD E,IXH
DD 5D            LD E,IXL
FD 5C            LD E,IYH
FD 5D            LD E,IYL
5D               LD E,L
DD CB :: 83      LD E,RES 0,(IX+::)
DD CB :: 8B      LD E,RES 1,(IX+::)
DD CB :: 93      LD E,RES 2,(IX+::)
DD CB :: 9B      LD E,RES 3,(IX+::)
DD CB :: A3      LD E,RES 4,(IX+::)
DD CB :: AB      LD E,RES 5,(IX+::)
DD CB :: B3      LD E,RES 6,(IX+::)
DD CB :: BB      LD E,RES 7,(IX+::)
FD CB :: 83      LD E,RES 0,(IY+::)
FD CB :: 8B      LD E,RES 1,(IY+::)
FD CB :: 93      LD E,RES 2,(IY+::)
FD CB :: 9B      LD E,RES 3,(IY+::)
FD CB :: A3      LD E,RES 4,(IY+::)
FD CB :: AB      LD E,RES 5,(IY+::)
FD CB :: B3      LD E,RES 6,(IY+::)
FD CB :: BB      LD E,RES 7,(IY+::)
DD CB :: 13      LD E,RL (IX+::)
FD CB :: 13      LD E,RL (IY+::)
DD CB :: 03      LD E,RLC (IX+::)
FD CB :: 03      LD E,RLC (IY+::)
DD CB :: 1B      LD E,RR (IX+::)
FD CB :: 1B      LD E,RR (IY+::)
DD CB :: 0B      LD E,RRC (IX+::)
FD CB :: 0B      LD E,RRC (IY+::)
DD CB :: C3      LD E,SET 0,(IX+::)
DD CB :: CB      LD E,SET 1,(IX+::)
DD CB :: D3      LD E,SET 2,(IX+::)
DD CB :: DB      LD E,SET 3,(IX+::)
DD CB :: E3      LD E,SET 4,(IX+::)
DD CB :: EB      LD E,SET 5,(IX+::)
DD CB :: F3      LD E,SET 6,(IX+::)
DD CB :: FB      LD E,SET 7,(IX+::)
FD CB :: C3      LD E,SET 0,(IY+::)
FD CB :: CB      LD E,SET 1,(IY+::)
FD CB :: D3      LD E,SET 2,(IY+::)
FD CB :: DB      LD E,SET 3,(IY+::)
FD CB :: E3      LD E,SET 4,(IY+::)
FD CB :: EB      LD E,SET 5,(IY+::)
FD CB :: F3      LD E,SET 6,(IY+::)
FD CB :: FB      LD E,SET 7,(IY+::)
DD CB :: 23      LD E,SLA (IX+::)
FD CB :: 23      LD E,SLA (IY+::)
DD CB :: 33      LD E,SLL (IX+::)
FD CB :: 33      LD E,SLL (IY+::)
DD CB :: 2B      LD E,SRA (IX+::)
FD CB :: 2B      LD E,SRA (IY+::)
DD CB :: 3B      LD E,SRL (IX+::)
FD CB :: 3B      LD E,SRL (IY+::)
26 ::            LD H,::
66               LD H,(HL)
DD 66 ::         LD H,(IX+::)
FD 66 ::         LD H,(IY+::)
67               LD H,A
60               LD H,B
61               LD H,C
62               LD H,D
63               LD H,E
64               LD H,H
65               LD H,L
DD CB :: 84      LD H,RES 0,(IX+::)
DD CB :: 8C      LD H,RES 1,(IX+::)
DD CB :: 94      LD H,RES 2,(IX+::)
DD CB :: 9C      LD H,RES 3,(IX+::)
DD CB :: A4      LD H,RES 4,(IX+::)
DD CB :: AC      LD H,RES 5,(IX+::)
DD CB :: B4      LD H,RES 6,(IX+::)
DD CB :: BC      LD H,RES 7,(IX+::)
FD CB :: 84      LD H,RES 0,(IY+::)
FD CB :: 8C      LD H,RES 1,(IY+::)
FD CB :: 94      LD H,RES 2,(IY+::)
FD CB :: 9C      LD H,RES 3,(IY+::)
FD CB :: A4      LD H,RES 4,(IY+::)
FD CB :: AC      LD H,RES 5,(IY+::)
FD CB :: B4      LD H,RES 6,(IY+::)
FD CB :: BC      LD H,RES 7,(IY+::)
DD CB :: 14      LD H,RL (IX+::)
FD CB :: 14      LD H,RL (IY+::)
DD CB :: 04      LD H,RLC (IX+::)
FD CB :: 04      LD H,RLC (IY+::)
DD CB :: 1C      LD H,RR (IX+::)
FD CB :: 1C      LD H,RR (IY+::)
DD CB :: 0C      LD H,RRC (IX+::)
FD CB :: 0C      LD H,RRC (IY+::)
DD CB :: C4      LD H,SET 0,(IX+::)
DD CB :: CC      LD H,SET 1,(IX+::)
DD CB :: D4      LD H,SET 2,(IX+::)
DD CB :: DC      LD H,SET 3,(IX+::)
DD CB :: E4      LD H,SET 4,(IX+::)
DD CB :: EC      LD H,SET 5,(IX+::)
DD CB :: F4      LD H,SET 6,(IX+::)
DD CB :: FC      LD H,SET 7,(IX+::)
FD CB :: C4      LD H,SET 0,(IY+::)
FD CB :: CC      LD H,SET 1,(IY+::)
FD CB :: D4      LD H,SET 2,(IY+::)
FD CB :: DC      LD H,SET 3,(IY+::)
FD CB :: E4      LD H,SET 4,(IY+::)
FD CB :: EC      LD H,SET 5,(IY+::)
FD CB :: F4      LD H,SET 6,(IY+::)
FD CB :: FC      LD H,SET 7,(IY+::)
DD CB :: 24      LD H,SLA (IX+::)
FD CB :: 24      LD H,SLA (IY+::)
DD CB :: 34      LD H,SLL (IX+::)
FD CB :: 34      LD H,SLL (IY+::)
DD CB :: 2C      LD H,SRA (IX+::)
FD CB :: 2C      LD H,SRA (IY+::)
DD CB :: 3C      LD H,SRL (IX+::)
FD CB :: 3C      LD H,SRL (IY+::)
2A :: ::         LD HL,(@@)
21 :: ::         LD HL,@@
ED 47            LD I,A
DD 2A :: ::      LD IX,(@@)
DD 21 :: ::      LD IX,@@
DD 26 ::         LD IXH,::
DD 67            LD IXH,A
DD 60            LD IXH,B
DD 61            LD IXH,C
DD 62            LD IXH,D
DD 63            LD IXH,E
DD 64            LD IXH,IXH
DD 65            LD IXH,IXL
DD 2E ::         LD IXL,::
DD 6F            LD IXL,A
DD 68            LD IXL,B
DD 69            LD IXL,C
DD 6A            LD IXL,D
DD 6B            LD IXL,E
DD 6C            LD IXL,IXH
DD 6D            LD IXL,IXL
FD 2A :: ::      LD IY,(@@)
FD 21 :: ::      LD IY,@@
FD 26 ::         LD IYH,::
FD 67            LD IYH,A
FD 60            LD IYH,B
FD 61            LD IYH,C
FD 62            LD IYH,D
FD 63            LD IYH,E
FD 64            LD IYH,IYH
FD 65            LD IYH,IYL
FD 2E ::         LD IYL,::
FD 6F            LD IYL,A
FD 68            LD IYL,B
FD 69            LD IYL,C
FD 6A            LD IYL,D
FD 6B            LD IYL,E
FD 6C            LD IYL,IYH
FD 6D            LD IYL,IYL
2E ::            LD L,::
6E               LD L,(HL)
DD 6E ::         LD L,(IX+::)
FD 6E ::         LD L,(IY+::)
6F               LD L,A
68               LD L,B
69               LD L,C
6A               LD L,D
6B               LD L,E
6C               LD L,H
6D               LD L,L
DD CB :: 85      LD L,RES 0,(IX+::)
DD CB :: 8D      LD L,RES 1,(IX+::)
DD CB :: 95      LD L,RES 2,(IX+::)
DD CB :: 9D      LD L,RES 3,(IX+::)
DD CB :: A5      LD L,RES 4,(IX+::)
DD CB :: AD      LD L,RES 5,(IX+::)
DD CB :: B5      LD L,RES 6,(IX+::)
DD CB :: BD      LD L,RES 7,(IX+::)
FD CB :: 85      LD L,RES 0,(IY+::)
FD CB :: 8D      LD L,RES 1,(IY+::)
FD CB :: 95      LD L,RES 2,(IY+::)
FD CB :: 9D      LD L,RES 3,(IY+::)
FD CB :: A5      LD L,RES 4,(IY+::)
FD CB :: AD      LD L,RES 5,(IY+::)
FD CB :: B5      LD L,RES 6,(IY+::)
FD CB :: BD      LD L,RES 7,(IY+::)
DD CB :: 15      LD L,RL (IX+::)
FD CB :: 15      LD L,RL (IY+::)
DD CB :: 05      LD L,RLC (IX+::)
FD CB :: 05      LD L,RLC (IY+::)
DD CB :: 1D      LD L,RR (IX+::)
FD CB :: 1D      LD L,RR (IY+::)
DD CB :: 0D      LD L,RRC (IX+::)
FD CB :: 0D      LD L,RRC (IY+::)
DD CB :: C5      LD L,SET 0,(IX+::)
DD CB :: CD      LD L,SET 1,(IX+::)
DD CB :: D5      LD L,SET 2,(IX+::)
DD CB :: DD      LD L,SET 3,(IX+::)
DD CB :: E5      LD L,SET 4,(IX+::)
DD CB :: ED      LD L,SET 5,(IX+::)
DD CB :: F5      LD L,SET 6,(IX+::)
DD CB :: FD      LD L,SET 7,(IX+::)
FD CB :: C5      LD L,SET 0,(IY+::)
FD CB :: CD      LD L,SET 1,(IY+::)
FD CB :: D5      LD L,SET 2,(IY+::)
FD CB :: DD      LD L,SET 3,(IY+::)
FD CB :: E5      LD L,SET 4,(IY+::)
FD CB :: ED      LD L,SET 5,(IY+::)
FD CB :: F5      LD L,SET 6,(IY+::)
FD CB :: FD      LD L,SET 7,(IY+::)
DD CB :: 25      LD L,SLA (IX+::)
FD CB :: 25      LD L,SLA (IY+::)
DD CB :: 35      LD L,SLL (IX+::)
FD CB :: 35      LD L,SLL (IY+::)
DD CB :: 2D      LD L,SRA (IX+::)
FD CB :: 2D      LD L,SRA (IY+::)
DD CB :: 3D      LD L,SRL (IX+::)
FD CB :: 3D      LD L,SRL (IY+::)
ED 7B :: ::      LD SP,(@@)
31 :: ::         LD SP,@@
F9               LD SP,HL
DD F9            LD SP,IX
FD F9            LD SP,IY
ED 4F            LD R,A
ED A8            LDD
ED B8            LDDR
ED A0            LDI
ED B0            LDIR
ED 44            NEG
00               NOP
F6 ::            OR ::
B6               OR (HL)
DD B6 ::         OR (IX+::)
FD B6 ::         OR (IY+::)
B7               OR A
B6               OR A,(HL)
B7               OR A,A
B0               OR A,B
B1               OR A,C
B2               OR A,D
B3               OR A,E
B4               OR A,H
B5               OR A,L
B0               OR B
B1               OR C
B2               OR D
B3               OR E
B4               OR H
DD B4            OR IXH
DD B5            OR IXL
FD B4            OR IYH
FD B5            OR IYL
B5               OR L
ED BB            OTDR
ED B3            OTIR
D3 ::            OUT (::),A
ED 71            OUT (C),0
ED 79            OUT (C),A
ED 41            OUT (C),B
ED 49            OUT (C),C
ED 51            OUT (C),D
ED 59            OUT (C),E
ED 61            OUT (C),H
ED 69            OUT (C),L
ED AB            OUTD
ED A3            OUTI
F1               POP AF
C1               POP BC
D1               POP DE
E1               POP HL
DD E1            POP IX
FD E1            POP IY
F5               PUSH AF
C5               PUSH BC
D5               PUSH DE
E5               PUSH HL
DD E5            PUSH IX
FD E5            PUSH IY
CB 86            RES 0,(HL)
CB 8E            RES 1,(HL)
CB 96            RES 2,(HL)
CB 9E            RES 3,(HL)
CB A6            RES 4,(HL)
CB AE            RES 5,(HL)
CB B6            RES 6,(HL)
CB BE            RES 7,(HL)
DD CB :: 86      RES 0,(IX+::)
DD CB :: 8E      RES 1,(IX+::)
DD CB :: 96      RES 2,(IX+::)
DD CB :: 9E      RES 3,(IX+::)
DD CB :: A6      RES 4,(IX+::)
DD CB :: AE      RES 5,(IX+::)
DD CB :: B6      RES 6,(IX+::)
DD CB :: BE      RES 7,(IX+::)
FD CB :: 86      RES 0,(IY+::)
FD CB :: 8E      RES 1,(IY+::)
FD CB :: 96      RES 2,(IY+::)
FD CB :: 9E      RES 3,(IY+::)
FD CB :: A6      RES 4,(IY+::)
FD CB :: AE      RES 5,(IY+::)
FD CB :: B6      RES 6,(IY+::)
FD CB :: BE      RES 7,(IY+::)
CB 87            RES 0,A
CB 8F            RES 1,A
CB 97            RES 2,A
CB 9F            RES 3,A
CB A7            RES 4,A
CB AF            RES 5,A
CB B7            RES 6,A
CB BF            RES 7,A
CB 80            RES 0,B
CB 88            RES 1,B
CB 90            RES 2,B
CB 98            RES 3,B
CB A0            RES 4,B
CB A8            RES 5,B
CB B0            RES 6,B
CB B8            RES 7,B
CB 81            RES 0,C
CB 89            RES 1,C
CB 91            RES 2,C
CB 99            RES 3,C
CB A1            RES 4,C
CB A9            RES 5,C
CB B1            RES 6,C
CB B9            RES 7,C
CB 82            RES 0,D
CB 8A            RES 1,D
CB 92            RES 2,D
CB 9A            RES 3,D
CB A2            RES 4,D
CB AA            RES 5,D
CB B2            RES 6,D
CB BA            RES 7,D
CB 83            RES 0,E
CB 8B            RES 1,E
CB 93            RES 2,E
CB 9B            RES 3,E
CB A3            RES 4,E
CB AB            RES 5,E
CB B3            RES 6,E
CB BB            RES 7,E
CB 84            RES 0,H
CB 8C            RES 1,H
CB 94            RES 2,H
CB 9C            RES 3,H
CB A4            RES 4,H
CB AC            RES 5,H
CB B4            RES 6,H
CB BC            RES 7,H
CB 85            RES 0,L
CB 8D            RES 1,L
CB 95            RES 2,L
CB 9D            RES 3,L
CB A5            RES 4,L
CB AD            RES 5,L
CB B5            RES 6,L
CB BD            RES 7,L
C9               RET
D8               RET C
F8               RET M
D0               RET NC
C0               RET NZ
F0               RET P
E8               RET PE
E0               RET PO
C8               RET Z
ED 4D            RETI
ED 45            RETN
CB 16            RL (HL)
DD CB :: 16      RL (IX+::)
FD CB :: 16      RL (IY+::)
CB 17            RL A
CB 10            RL B
CB 11            RL C
CB 12            RL D
CB 13            RL E
CB 14            RL H
CB 15            RL L
17               RLA
CB 06            RLC (HL)
DD CB :: 06      RLC (IX+::)
FD CB :: 06      RLC (IY+::)
CB 07            RLC A
CB 00            RLC B
CB 01            RLC C
CB 02            RLC D
CB 03            RLC E
CB 04            RLC H
CB 05            RLC L
07               RLCA
ED 6F            RLD
CB 1E            RR (HL)
DD CB :: 1E      RR (IX+::)
FD CB :: 1E      RR (IY+::)
CB 1F            RR A
CB 18            RR B
CB 19            RR C
CB 1A            RR D
CB 1B            RR E
CB 1C            RR H
CB 1D            RR L
1F               RRA
CB 0E            RRC (HL)
DD CB :: 0E      RRC (IX+::)
FD CB :: 0E      RRC (IY+::)
CB 0F            RRC A
CB 08            RRC B
CB 09            RRC C
CB 0A            RRC D
CB 0B            RRC E
CB 0C            RRC H
CB 0D            RRC L
0F               RRCA
ED 67            RRD
C7               RST 0X00
CF               RST 0X08
D7               RST 0X10
DF               RST 0X18
E7               RST 0X20
EF               RST 0X28
F7               RST 0X30
FF               RST 0X38
DE ::            SBC A,::
9E               SBC A,(HL)
DD 9E ::         SBC A,(IX+::)
FD 9E ::         SBC A,(IY+::)
9F               SBC A,A
98               SBC A,B
99               SBC A,C
9A               SBC A,D
9B               SBC A,E
9C               SBC A,H
DD 9C            SBC A,IXH
DD 9D            SBC A,IXL
FD 9C            SBC A,IYH
FD 9D            SBC A,IYL
9D               SBC A,L
ED 42            SBC HL,BC
ED 52            SBC HL,DE
ED 62            SBC HL,HL
ED 72            SBC HL,SP
37               SCF
CB C6            SET 0,(HL)
CB CE            SET 1,(HL)
CB D6            SET 2,(HL)
CB DE            SET 3,(HL)
CB E6            SET 4,(HL)
CB EE            SET 5,(HL)
CB F6            SET 6,(HL)
CB FE            SET 7,(HL)
DD CB :: C6      SET 0,(IX+::)
DD CB :: CE      SET 1,(IX+::)
DD CB :: D6      SET 2,(IX+::)
DD CB :: DE      SET 3,(IX+::)
DD CB :: E6      SET 4,(IX+::)
DD CB :: EE      SET 5,(IX+::)
DD CB :: F6      SET 6,(IX+::)
DD CB :: FE      SET 7,(IX+::)
FD CB :: C6      SET 0,(IY+::)
FD CB :: CE      SET 1,(IY+::)
FD CB :: D6      SET 2,(IY+::)
FD CB :: DE      SET 3,(IY+::)
FD CB :: E6      SET 4,(IY+::)
FD CB :: EE      SET 5,(IY+::)
FD CB :: F6      SET 6,(IY+::)
FD CB :: FE      SET 7,(IY+::)
CB C7            SET 0,A
CB CF            SET 1,A
CB D7            SET 2,A
CB DF            SET 3,A
CB E7            SET 4,A
CB EF            SET 5,A
CB F7            SET 6,A
CB FF            SET 7,A
CB C0            SET 0,B
CB C8            SET 1,B
CB D0            SET 2,B
CB D8            SET 3,B
CB E0            SET 4,B
CB E8            SET 5,B
CB F0            SET 6,B
CB F8            SET 7,B
CB C1            SET 0,C
CB C9            SET 1,C
CB D1            SET 2,C
CB D9            SET 3,C
CB E1            SET 4,C
CB E9            SET 5,C
CB F1            SET 6,C
CB F9            SET 7,C
CB C2            SET 0,D
CB CA            SET 1,D
CB D2            SET 2,D
CB DA            SET 3,D
CB E2            SET 4,D
CB EA            SET 5,D
CB F2            SET 6,D
CB FA            SET 7,D
CB C3            SET 0,E
CB CB            SET 1,E
CB D3            SET 2,E
CB DB            SET 3,E
CB E3            SET 4,E
CB EB            SET 5,E
CB F3            SET 6,E
CB FB            SET 7,E
CB C4            SET 0,H
CB CC            SET 1,H
CB D4            SET 2,H
CB DC            SET 3,H
CB E4            SET 4,H
CB EC            SET 5,H
CB F4            SET 6,H
CB FC            SET 7,H
CB C5            SET 0,L
CB CD            SET 1,L
CB D5            SET 2,L
CB DD            SET 3,L
CB E5            SET 4,L
CB ED            SET 5,L
CB F5            SET 6,L
CB FD            SET 7,L
CB 26            SLA (HL)
DD CB :: 26      SLA (IX+::)
FD CB :: 26      SLA (IY+::)
CB 27            SLA A
CB 20            SLA B
CB 21            SLA C
CB 22            SLA D
CB 23            SLA E
CB 24            SLA H
CB 25            SLA L
CB 36            SLL (HL)
DD CB :: 36      SLL (IX+::)
FD CB :: 36      SLL (IY+::)
CB 37            SLL A
CB 30            SLL B
CB 31            SLL C
CB 32            SLL D
CB 33            SLL E
CB 34            SLL H
CB 35            SLL L
CB 2E            SRA (HL)
DD CB :: 2E      SRA (IX+::)
FD CB :: 2E      SRA (IY+::)
CB 2F            SRA A
CB 28            SRA B
CB 29            SRA C
CB 2A            SRA D
CB 2B            SRA E
CB 2C            SRA H
CB 2D            SRA L
CB 3E            SRL (HL)
DD CB :: 3E      SRL (IX+::)
FD CB :: 3E      SRL (IY+::)
CB 3F            SRL A
CB 38            SRL B
CB 39            SRL C
CB 3A            SRL D
CB 3B            SRL E
CB 3C            SRL H
CB 3D            SRL L
D6 ::            SUB ::
96               SUB (HL)
DD 96 ::         SUB (IX+::)
FD 96 ::         SUB (IY+::)
97               SUB A
96               SUB A,(HL)
97               SUB A,A
90               SUB A,B
91               SUB A,C
92               SUB A,D
93               SUB A,E
94               SUB A,H
95               SUB A,L
90               SUB B
91               SUB C
92               SUB D
93               SUB E
94               SUB H
DD 94            SUB IXH
DD 95            SUB IXL
FD 94            SUB IYH
FD 95            SUB IYL
95               SUB L
EE ::            XOR ::
AE               XOR (HL)
DD AE ::         XOR (IX+::)
FD AE ::         XOR (IY+::)
AF               XOR A
AE               XOR A,(HL)
AF               XOR A,A
A8               XOR A,B
A9               XOR A,C
AA               XOR A,D
AB               XOR A,E
AC               XOR A,H
AD               XOR A,L
A8               XOR B
A9               XOR C
AA               XOR D
AB               XOR E
AC               XOR H
DD AC            XOR IXH
DD AD            XOR IXL
FD AC            XOR IYH
FD AD            XOR IYL
AD               XOR L
'''

instructions = {}


def create_pattern(candidate):
    """
    Create search pattern for parameter placeholders

    :param candidate: Instruction template
    :return: Regular expression pattern for matching
    """
    types = []
    pat = '@@|::|%%'
    while True:
        m = re.search(pat, candidate)
        if m:
            s = m.span()
            types.append(candidate[s[0]:s[1]])
            replacement = num_label
            candidate = candidate[0:s[0]] + replacement + candidate[s[1]:]
        else:
            break
    return re.compile(candidate + "$"), types




def preprocess():
    lines = db.split('\n')
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if len(l) > 0]
    for line in lines:
        code = line[0:17].strip()
        inst = line[17:]
        mnemonic = inst.split()[0]
        if mnemonic not in instructions:
            instructions[mnemonic] = []
        inst,types=create_pattern(re.escape(inst))
        instructions[mnemonic].append((code, inst, types))


def get_instructions(mnemonic):
    if len(instructions) == 0:
        preprocess()
    return instructions.get(mnemonic.upper())
