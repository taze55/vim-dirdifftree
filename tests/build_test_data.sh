#!/bin/bash

# Vim global plugin for diff two directories and represent them as a tree
# Maintainer: taze55 <taze_a28391214@icloud.com>
# URL: https://github.com/taze55/vim-dirdifftree

# https://stackoverflow.com/questions/3349105/how-can-i-set-the-current-working-directory-to-the-directory-of-the-script-in-ba
cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")"

mkdir -p test_data
cd test_data

# For buildTree and renderNode test
mkdir -p test_1xx/left
mkdir -p test_1xx/right

mkdir -p test_2xx/left
mkdir -p test_2xx/right
touch    test_2xx/left/a
touch    test_2xx/left/b
touch    test_2xx/left/c

mkdir -p test_3xx/left
mkdir -p test_3xx/right
touch    test_3xx/right/a
touch    test_3xx/right/b
touch    test_3xx/right/c

mkdir -p test_4xx/left
mkdir -p test_4xx/right
touch    test_4xx/left/a
touch    test_4xx/left/c
touch    test_4xx/right/b
touch    test_4xx/right/c

mkdir -p test_5xx/left
mkdir -p test_5xx/right
mkdir -p test_5xx/left/A
mkdir -p test_5xx/left/B
mkdir -p test_5xx/left/C

mkdir -p test_6xx/left
mkdir -p test_6xx/right
mkdir -p test_6xx/right/A
mkdir -p test_6xx/right/B
mkdir -p test_6xx/right/C

mkdir -p test_7xx/left
mkdir -p test_7xx/right
mkdir -p test_7xx/left/A
mkdir -p test_7xx/left/C
mkdir -p test_7xx/right/B
mkdir -p test_7xx/right/C

mkdir -p test_8xx/left
mkdir -p test_8xx/right
mkdir -p test_8xx/left/A
touch    test_8xx/left/A/a
mkdir -p test_8xx/left/B
touch    test_8xx/left/B/a
touch    test_8xx/left/B/b
mkdir -p test_8xx/left/C
touch    test_8xx/left/C/a
touch    test_8xx/left/C/b
touch    test_8xx/left/C/c

mkdir -p test_9xx/left
mkdir -p test_9xx/right
mkdir -p test_9xx/right/A
touch    test_9xx/right/A/a
mkdir -p test_9xx/right/B
touch    test_9xx/right/B/a
touch    test_9xx/right/B/b
mkdir -p test_9xx/right/C
touch    test_9xx/right/C/a
touch    test_9xx/right/C/b
touch    test_9xx/right/C/c

mkdir -p test_10xx/left
mkdir -p test_10xx/right
mkdir -p test_10xx/left/A
touch    test_10xx/left/A/a
mkdir -p test_10xx/left/B
touch    test_10xx/left/B/a
mkdir -p test_10xx/left/C
touch    test_10xx/left/C/a
touch    test_10xx/left/C/c
mkdir -p test_10xx/right/A
touch    test_10xx/right/A/a
mkdir -p test_10xx/right/B
touch    test_10xx/right/B/b
mkdir -p test_10xx/right/C
touch    test_10xx/right/C/b
touch    test_10xx/right/C/c

mkdir -p test_11xx/left
mkdir -p test_11xx/right
mkdir -p test_11xx/left/right/right/right/right
touch    test_11xx/left/left
touch    test_11xx/left/right/left
touch    test_11xx/left/right/right/left
touch    test_11xx/left/right/right/right/left
mkdir -p test_11xx/right/right/right/right/right
touch    test_11xx/right/left
touch    test_11xx/right/right/left
touch    test_11xx/right/right/right/left
touch    test_11xx/right/right/right/right/left

mkdir -p test_12xx/left
mkdir -p test_12xx/right
mkdir -p test_12xx/left/A/B/C/D
mkdir -p test_12xx/right/A/B/C/D

mkdir -p test_13xx/left
mkdir -p test_13xx/right
mkdir -p test_13xx/left/A/B/C/D
touch    test_13xx/left/A/B/C/D/a
touch    test_13xx/left/A/B/C/D/c
mkdir -p test_13xx/right/A/B/C/D
touch    test_13xx/right/A/B/C/D/b
touch    test_13xx/right/A/B/C/D/c

mkdir -p test_14xx/left
mkdir -p test_14xx/right
mkdir -p test_14xx/left/A/B/C/D
touch    test_14xx/left/A/B/C/D/a
mkdir -p test_14xx/left/A/B/C/D/E/F/G/H
touch    test_14xx/left/A/B/C/D/E/F/G/H/a
mkdir -p test_14xx/left/I/J/K/L
mkdir -p test_14xx/right/A/B/C/D
touch    test_14xx/right/A/B/C/D/a
mkdir -p test_14xx/right/A/B/C/D/E/F/G/H
touch    test_14xx/right/A/B/C/D/E/F/G/H/a
mkdir -p test_14xx/right/I/J/K/L

mkdir -p test_15xx/left
mkdir -p test_15xx/right
mkdir -p test_15xx/left/A/B/C/D/E

mkdir -p test_16xx/left
mkdir -p test_16xx/right
mkdir -p test_16xx/left/A/B/C
mkdir -p test_16xx/right/A/B/C/D/E

mkdir -p test_17xx/left
mkdir -p test_17xx/right
mkdir -p test_17xx/left/A/B/C
mkdir -p test_17xx/left/I/J/K/L
touch    test_17xx/left/I/J/K/L/a
mkdir -p test_17xx/right/A/B/C/D/E/F/G/H
touch    test_17xx/right/A/B/C/D/a
touch    test_17xx/right/A/B/C/D/E/F/G/H/a
mkdir -p test_17xx/right/I/J

mkdir -p test_18xx/left
mkdir -p test_18xx/right
mkdir -p test_18xx/left/Z
mkdir -p test_18xx/left/CCC
mkdir -p test_18xx/left/B
mkdir -p test_18xx/left/AA
mkdir -p test_18xx/left/A
touch    test_18xx/left/9
touch    test_18xx/left/333
touch    test_18xx/left/2
touch    test_18xx/left/11
touch    test_18xx/left/1
mkdir -p test_18xx/right/Z
mkdir -p test_18xx/right/CCC
mkdir -p test_18xx/right/B
mkdir -p test_18xx/right/AA
mkdir -p test_18xx/right/A
touch    test_18xx/right/9
touch    test_18xx/right/333
touch    test_18xx/right/2
touch    test_18xx/right/11
touch    test_18xx/right/1

mkdir -p test_19xx/left
mkdir -p test_19xx/right
mkdir -p test_19xx/left/A/B/C
mkdir -p test_19xx/right/A/B/C

mkdir -p test_20xx/left
mkdir -p test_20xx/right
mkdir -p test_20xx/left/A/B/C
touch    test_20xx/left/A/B/C/1
touch    test_20xx/left/A/B/C/11
mkdir -p test_20xx/right/A/B/C
touch    test_20xx/right/A/B/C/1
touch    test_20xx/right/A/B/C/z

mkdir -p test_21xx/left
mkdir -p test_21xx/right

mkdir -p test_21xx/left/A/B/D/E
mkdir -p test_21xx/left/A/B/F/G
mkdir -p test_21xx/left/A/B/I/J/K
mkdir -p test_21xx/left/A/B/L/M/N
mkdir -p test_21xx/left/O/P/Q/R
touch    test_21xx/left/1
touch    test_21xx/left/11
touch    test_21xx/left/z
touch    test_21xx/left/A/11
touch    test_21xx/left/A/z
touch    test_21xx/left/A/B/D/E/11
touch    test_21xx/left/A/B/D/E/z
touch    test_21xx/left/A/B/I/J/K/1
touch    test_21xx/left/A/B/I/J/K/11
touch    test_21xx/left/A/B/I/J/K/z
touch    test_21xx/left/O/1
touch    test_21xx/left/O/11

mkdir -p test_21xx/right/A/B/C
mkdir -p test_21xx/right/A/B/D/E
mkdir -p test_21xx/right/A/B/F/G/H
mkdir -p test_21xx/right/A/B/I
mkdir -p test_21xx/right/A/B/L/M/N
mkdir -p test_21xx/right/O/P/Q
touch    test_21xx/right/1
touch    test_21xx/right/11
touch    test_21xx/right/A/1
touch    test_21xx/right/A/11
touch    test_21xx/right/A/z
touch    test_21xx/right/A/B/C/1
touch    test_21xx/right/A/B/C/11
touch    test_21xx/right/A/B/C/z
touch    test_21xx/right/A/B/D/E/1
touch    test_21xx/right/A/B/D/E/z
touch    test_21xx/right/A/B/F/G/H/1
touch    test_21xx/right/A/B/F/G/H/11
touch    test_21xx/right/A/B/F/G/H/z
touch    test_21xx/right/O/1
touch    test_21xx/right/O/z

mkdir -p test_22xx/left
mkdir -p test_22xx/right
mkdir -p test_22xx/left/.git
touch    test_22xx/left/.git/1
mkdir -p test_22xx/left/__pycache__
mkdir -p test_22xx/right/node_modules
touch    test_22xx/right/node_modules/2

mkdir -p test_23xx/left
mkdir -p test_23xx/right
mkdir -p test_23xx/left/A/.git/B/C
touch    test_23xx/left/A/1
touch    test_23xx/left/A/.git/2
touch    test_23xx/left/A/.git/B/3
touch    test_23xx/left/A/.git/B/C/4
mkdir -p test_23xx/right/A/B/C/node_modules/D/E
touch    test_23xx/right/A/1
touch    test_23xx/right/A/B/C/2
touch    test_23xx/right/A/B/C/node_modules/3
touch    test_23xx/right/A/B/C/node_modules/D/4
touch    test_23xx/right/A/B/C/node_modules/D/E/5

mkdir -p test_24xx/left
mkdir -p test_24xx/right
mkdir -p test_24xx/left/A/AAA/B/C
touch    test_24xx/left/A/1
touch    test_24xx/left/A/AAA/2
touch    test_24xx/left/A/AAA/B/3
touch    test_24xx/left/A/AAA/B/C/4
mkdir -p test_24xx/right/A/B/C/BBB/D/E
touch    test_24xx/right/A/1
touch    test_24xx/right/A/B/C/2
touch    test_24xx/right/A/B/C/BBB/3
touch    test_24xx/right/A/B/C/BBB/D/4
touch    test_24xx/right/A/B/C/BBB/D/E/5

mkdir -p test_25xx/left
mkdir -p test_25xx/right
mkdir -p test_25xx/left/a
touch    test_25xx/left/a/b
mkdir -p test_25xx/left/C
touch    test_25xx/left/C/D
mkdir -p test_25xx/left/E
touch    test_25xx/left/E/f
mkdir -p test_25xx/left/I
touch    test_25xx/left/I/J
mkdir -p test_25xx/left/G
touch    test_25xx/left/G/H
mkdir -p test_25xx/right/A
touch    test_25xx/right/A/B
mkdir -p test_25xx/right/c
touch    test_25xx/right/c/d
mkdir -p test_25xx/right/E
touch    test_25xx/right/E/F
mkdir -p test_25xx/right/g
touch    test_25xx/right/g/H
mkdir -p test_25xx/right/I
touch    test_25xx/right/I/J

# For normalizeDirectory test
mkdir -p test_n1

mkdir -p test_n2

# mkdir -p test_n3

# Symbolic link test
mkdir -p test_s1/left
mkdir -p test_s1/right
mkdir -p test_s1/left/A
ln -s    test_s1/left/A test_s1/left/A/B
mkdir -p test_s1/right/A
ln -s    test_s1/right/A test_s1/right/A/B
