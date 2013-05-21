

create database IF NOT EXISTS df;
grant all privileges on df.* to df@localhost identified by 'df';
USE df;
--
-- Database: `df`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_group`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_group_permissions`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_message`
--

CREATE TABLE IF NOT EXISTS `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_message`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add message', 4, 'add_message'),
(11, 'Can change message', 4, 'change_message'),
(12, 'Can delete message', 4, 'delete_message'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add log entry', 7, 'add_logentry'),
(20, 'Can change log entry', 7, 'change_logentry'),
(21, 'Can delete log entry', 7, 'delete_logentry'),
(22, 'Can add logged in user', 8, 'add_loggedinuser'),
(23, 'Can change logged in user', 8, 'change_loggedinuser'),
(24, 'Can delete logged in user', 8, 'delete_loggedinuser'),
(25, 'Can add rule', 9, 'add_rule'),
(26, 'Can change rule', 9, 'change_rule'),
(27, 'Can delete rule', 9, 'delete_rule');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`) VALUES
(6, 'django', '', '', '', 'sha1$d9802$5b91c3021dc5ac137f2280ca8f026c69edf55df0', 0, 1, 0, '2013-05-19 01:15:43', '2013-05-13 12:44:53'),
(4, 'espen', '', '', '', 'sha1$fc613$80217fd86cf4a3754930bc39276d03e0f2504c16', 1, 1, 1, '2013-05-19 01:15:19', '2013-04-24 15:30:58'),
(8, 'svein', '', '', '', 'sha1$64638$e94573c64f1266d5482f8104c046848c4fe6d6d9', 0, 1, 0, '2013-05-18 23:43:01', '2013-05-15 09:18:56');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_user_groups`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_user_user_permissions`
--


-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE IF NOT EXISTS `clients` (
  `user` varchar(80) DEFAULT NULL,
  `mac` varchar(80) DEFAULT NULL,
  `ip4` varchar(80) DEFAULT NULL,
  `ip6` varchar(80) DEFAULT NULL,
  `active` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`user`, `mac`, `ip4`, `ip6`, `active`) VALUES
('espen', '08:00:27:9a:ce:72', '10.0.0.100', 'Not in use', 0),
('django', '08:00:27:9a:ce:72', '10.0.0.100', 'Not in use', 1),
('svein', '08:00:27:9a:ce:72', '10.0.0.100', 'Not in use', 0);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `user_id`, `content_type_id`, `object_id`, `object_repr`, `action_flag`, `change_message`) VALUES
(1, '2013-05-13 12:01:49', 4, 3, '5', 'djangologin', 1, ''),
(2, '2013-05-13 12:08:47', 4, 3, '5', 'django', 2, 'Endret username og password.'),
(3, '2013-05-13 12:15:48', 4, 3, '5', 'django', 2, 'Ingen felt endret.'),
(4, '2013-05-15 09:17:51', 4, 3, '7', 'svein', 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'message', 'auth', 'message'),
(5, 'content type', 'contenttypes', 'contenttype'),
(6, 'session', 'sessions', 'session'),
(7, 'log entry', 'admin', 'logentry'),
(8, 'logged in user', 'login', 'loggedinuser'),
(9, 'rule', 'manager', 'rule');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('57378513b7aebf42b00d56138dc33bc5', 'gAJ9cQEuNzQ5MjVkYjdjZGEyNGE5Y2ZkYjI3NWM0MThkNWVmYjg=\n', '2013-05-05 22:54:23'),
('652dc218006669b1290a2c3525edf826', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUhZERORi5sb2dpbi5taWdyYXRlLkZpcnN0TG9n\naW5BdXRocQNVDV9hdXRoX3VzZXJfaWRxBIoBAnUuMmMxZGNjYmZlYWEyZDljNzkxMDc2OTJhNTA2\nNjFiYWE=\n', '2013-05-06 16:03:11'),
('9c5551e93fa39c1e006050449fc4dcc8', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-02 00:36:24'),
('af44876bf74197f3e8944a26438b0279', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUhZERORi5sb2dpbi5taWdyYXRlLkZpcnN0TG9n\naW5BdXRocQNVDV9hdXRoX3VzZXJfaWRxBIoBAnUuMmMxZGNjYmZlYWEyZDljNzkxMDc2OTJhNTA2\nNjFiYWE=\n', '2013-05-06 16:06:57'),
('55c553dfce07f44670b0876cc94b8635', 'gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQKKAQJVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSFkRE5GLmxv\nZ2luLm1pZ3JhdGUuRmlyc3RMb2dpbkF1dGhxBHUuZDlhMzRiMzhhNmEwNjc2ZDIzZjBhZDY4OWE2\nYmVlNTM=\n', '2013-05-08 12:48:13'),
('578732d9f7c7658353faece387f3cb53', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUhZERORi5sb2dpbi5taWdyYXRlLkZpcnN0TG9n\naW5BdXRocQNVDV9hdXRoX3VzZXJfaWRxBIoBBHUuYjI2NTk2MzFhZTNmNDVhNGRlM2FhYzVmMmJj\nMzU4MTU=\n', '2013-05-16 10:52:14'),
('6fe3c348c2904b99b5f9545d864bf815', 'gAJ9cQEuNzQ5MjVkYjdjZGEyNGE5Y2ZkYjI3NWM0MThkNWVmYjg=\n', '2013-05-29 09:20:48'),
('b2ad5968b907d9a11629847324e61084', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 20:54:55'),
('976164ca5e7f7979475f3bd72fb854b0', 'gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQKKAQRVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSBkRE5GLmxv\nZ2luLm1pZ3JhdGUuRGphbmdvREJMb2dpbnEEdS43YTU1ZTc3MDJiYjgwMWFhMzAzZTFiYjQ3ODNk\nYTZjYg==\n', '2013-06-02 01:12:26'),
('19b0e0e2cc42522abac6358019e4a41a', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 21:06:49'),
('67281365429f67f2537916ec1be1a047', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:42:36'),
('e684e2e029a33d175bba195600cc3a08', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:50:21'),
('18698b9563d2c5adcda1aa7fc4c8fe43', 'gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQKKAQRVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSBkRE5GLmxv\nZ2luLm1pZ3JhdGUuRGphbmdvREJMb2dpbnEEdS43YTU1ZTc3MDJiYjgwMWFhMzAzZTFiYjQ3ODNk\nYTZjYg==\n', '2013-06-01 23:55:28'),
('ad1be99cb766379a94f8e2266a978c3f', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:58:17'),
('235f991eba612179242f0f87e96372e4', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:49:14'),
('7a3805ff2e8a0630f1e669f28e97366c', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-02 00:50:12'),
('a3e5869fb7efa62ed0dc31f98413dcd1', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:57:23'),
('bc591c24a402315fb845bbdb9542c795', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEEdS5mZmNlYTJmMmQ3OWE2ZDgzM2ViMWQ5ZmIwNDdm\nNzc1Zg==\n', '2013-06-01 23:59:13'),
('68a3700cfab6bdfe5f424d2265d45cc6', 'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUgZERORi5sb2dpbi5taWdyYXRlLkRqYW5nb0RC\nTG9naW5xA1UNX2F1dGhfdXNlcl9pZHEEigEGdS5hYzgwZjY3NGMzZTEzM2M3YjNkZTI5YjBlOTU2\nMWIxMw==\n', '2013-06-02 01:15:43'),
('f127efb2109f4879641e0b3b6462fb7a', 'gAJ9cQEuNzQ5MjVkYjdjZGEyNGE5Y2ZkYjI3NWM0MThkNWVmYjg=\n', '2013-06-02 01:15:31'),
('207ac3223718d0d44ac9d3c3b8f91516', 'gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQKKAQRVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSBkRE5GLmxv\nZ2luLm1pZ3JhdGUuRGphbmdvREJMb2dpbnEEdS43YTU1ZTc3MDJiYjgwMWFhMzAzZTFiYjQ3ODNk\nYTZjYg==\n', '2013-06-02 00:34:52');

-- --------------------------------------------------------

--
-- Table structure for table `limited`
--

CREATE TABLE IF NOT EXISTS `limited` (
  `User` varchar(255) DEFAULT NULL,
  `CONNLIMIT` int(8) DEFAULT NULL,
  `RXLIMIT` int(8) DEFAULT NULL,
  `TXLIMIT` int(8) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `limited`
--

INSERT IGNORE INTO `limited` (`User`, `CONNLIMIT`, `RXLIMIT`, `TXLIMIT`) VALUES
('espen', 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `login_loggedinuser`
--

CREATE TABLE IF NOT EXISTS `login_loggedinuser` (
  `user_ptr_id` int(11) NOT NULL,
  `last_seen_ip` char(15) NOT NULL,
  PRIMARY KEY (`user_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login_loggedinuser`
--

INSERT IGNORE INTO `login_loggedinuser` (`user_ptr_id`, `last_seen_ip`) VALUES
(4, '10.0.0.100'),
(6, '10.0.0.100'),
(8, '10.0.0.100');

-- --------------------------------------------------------

--
-- Table structure for table `manager_rule`
--

CREATE TABLE IF NOT EXISTS `manager_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chain` varchar(7) NOT NULL,
  `prot` varchar(3) DEFAULT NULL,
  `src` varchar(20) NOT NULL,
  `spt` varchar(5) DEFAULT NULL,
  `dst` varchar(20) DEFAULT NULL,
  `dpt` varchar(5) DEFAULT NULL,
  `action` varchar(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `manager_rule`
--

INSERT IGNORE INTO `manager_rule` (`id`, `chain`, `prot`, `src`, `spt`, `dst`, `dpt`, `action`) VALUES
(3, 'FORWARD', 'TCP', '182.123.23.1/32', '22', '1.2.3.4/32', '44', 'DROP'),
(4, 'FORWARD', 'TCP', '0.0.0.0/32', NULL, '', '25', 'DROP'),
(5, 'INPUT', 'TCP', '10.10.10.1/32', '22', '', NULL, 'ACCEPT');

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE IF NOT EXISTS `stats` (
  `user` varchar(80) DEFAULT NULL,
  `connections` bigint(255) DEFAULT NULL,
  `tx_total` bigint(255) DEFAULT NULL,
  `rx_total` bigint(255) DEFAULT NULL,
  `txs` bigint(255) DEFAULT NULL,
  `rxs` bigint(255) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stats`
--

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
