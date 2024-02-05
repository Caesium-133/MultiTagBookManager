/*
 Navicat Premium Data Transfer

 Source Server         : booksManage
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 05/02/2024 20:06:16
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for book_tag
-- ----------------------------
DROP TABLE IF EXISTS "book_tag";
CREATE TABLE "book_tag" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "book_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY ("book_id") REFERENCES "books" ("book_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("tag_id") REFERENCES "tags" ("tag_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("book_id" ASC, "tag_id" ASC)
);

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS "books";
CREATE TABLE "books" (
  "book_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "url" TEXT,
  "name" TEXT,
  "author" TEXT,
  "rating" INTEGER DEFAULT 0,
  "status" TEXT DEFAULT '未完结',
  "read_status" TEXT DEFAULT '未读',
  "updated_chapter" TEXT,
  "last_update_date" TEXT DEFAULT CURRENT_DATE,
  "website" TEXT,
  "comment" TEXT
);

-- ----------------------------
-- Table structure for categories1st
-- ----------------------------
DROP TABLE IF EXISTS "categories1st";
CREATE TABLE "categories1st" (
  "cat1_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "cat1_name" TEXT NOT NULL
);

-- ----------------------------
-- Table structure for categories2nd
-- ----------------------------
DROP TABLE IF EXISTS "categories2nd";
CREATE TABLE "categories2nd" (
  "cat2_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "cat2_name" TEXT NOT NULL,
  "cat1_id" INTEGER,
  FOREIGN KEY ("cat1_id") REFERENCES "categories1st" ("cat1_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Table structure for categories3rd
-- ----------------------------
DROP TABLE IF EXISTS "categories3rd";
CREATE TABLE "categories3rd" (
  "cat3_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "cat3_name" TEXT NOT NULL,
  "cat2_id" INTEGER,
  FOREIGN KEY ("cat2_id") REFERENCES "categories2nd" ("cat2_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS "tags";
CREATE TABLE "tags" (
  "tag_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "tag_name" TEXT NOT NULL
);

-- ----------------------------
-- Auto increment value for book_tag
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 15 WHERE name = 'book_tag';

-- ----------------------------
-- Auto increment value for books
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'books';

-- ----------------------------
-- Auto increment value for tags
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 12 WHERE name = 'tags';

PRAGMA foreign_keys = true;
