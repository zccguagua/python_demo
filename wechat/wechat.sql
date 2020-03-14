/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50725
Source Host           : localhost:3306
Source Database       : wechat

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2020-03-15 02:22:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for contacts
-- ----------------------------
DROP TABLE IF EXISTS `contacts`;
CREATE TABLE `contacts` (
  `nickname` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '昵称',
  `username` varchar(108) DEFAULT NULL COMMENT '名称id（每次会变）',
  `remarkname` varchar(32) DEFAULT NULL COMMENT '备注名',
  `signature` varchar(1024) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '个性签名',
  `province` varchar(64) DEFAULT NULL,
  `city` varchar(16) DEFAULT NULL,
  `membercount` varchar(8) DEFAULT NULL COMMENT '人数',
  `sex` varchar(4) DEFAULT NULL,
  `attrstatus` varchar(16) DEFAULT NULL,
  `snsflag` varchar(8) DEFAULT NULL,
  `contactflag` varchar(16) DEFAULT NULL,
  `headimgurl` varchar(256) DEFAULT NULL,
  `time` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `nickname` varchar(64) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '昵称',
  `username` varchar(108) DEFAULT NULL COMMENT '名称id（每次会变）',
  `remarkname` varchar(32) DEFAULT NULL COMMENT '备注名',
  `signature` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '个性签名',
  `province` varchar(64) DEFAULT NULL,
  `city` varchar(16) DEFAULT NULL,
  `membercount` varchar(8) DEFAULT NULL COMMENT '人数',
  `sex` varchar(4) DEFAULT NULL,
  `attrstatus` varchar(16) DEFAULT NULL,
  `snsflag` varchar(8) DEFAULT NULL,
  `contactflag` varchar(16) DEFAULT NULL,
  `headimgurl` varchar(256) DEFAULT NULL,
  `time` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
