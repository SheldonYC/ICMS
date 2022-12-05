SET SQL_MODE = `NO_AUTO_VALUE_ON_ZERO`;
SET time_zone = `+00:00`;

-- Database: `facerecognition`
-- Drop previous tables
DROP TABLE IF EXISTS `Action`;
DROP TABLE IF EXISTS `Enroll`;
DROP TABLE IF EXISTS `Student`;
DROP TABLE IF EXISTS `Class`;
DROP TABLE IF EXISTS `Course`;

-- Table structure for table `Student`

CREATE TABLE `Student` (
  `student_id` int NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY(`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Student` VALUES (1, "JACK", "u3569274@connect.hku.hk");

-- Table structure for table `Action`

Create TABLE `Action` (
  `action_id` int NOT NULL,
  `student_id` int NOT NULL,
  `action_name` varchar(15) NOT NULL,
  `datetime` DATETIME NOT NULL,
  PRIMARY KEY(`action_id`, `datetime`),
  FOREIGN KEY(`student_id`) REFERENCES Student (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Action` VALUES (0, 1, "Sign in", "2022-11-13 22:10:53");
INSERT INTO `Action` VALUES (2, 1, "View class", "2022-11-13 22:11:02");
INSERT INTO `Action` VALUES (3, 1, "Send email", "2022-11-13 22:11:09");
INSERT INTO `Action` VALUES (1, 1, "Sign out", "2022-11-13 23:11:24");

-- Table structure for table `Course`

Create TABLE `Course` (
  `course_id` varchar(10) NOT NULL,
  `course_name` varchar(50) NOT NULL,
  `teacher_name` varchar(50) NOT NULL,
  `supplementary_material` varchar(100) NOT NULL, -- Things like textbook link that cannot be shared due to IP, and stayed the same through the semester
  `teacher_message` varchar(100) NOT NULL, -- some remarks from teacher for next lecture/tutorials
  PRIMARY KEY(`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Course` VALUES ("COMP3278", "Introduction to Database", "Mr. Ming Xiao", "You may checkout reference textbook Introduction to DBMS for 3 years old", "Today is our final in-class test, please come to lecture hall on time!");
INSERT INTO `Course` VALUES ("COMP2119", "Introduction to Data Structures and Algorithms", "Dr. Hao Hao", "Found this funny cat video: www.youtube.com/cutecats", "Today we will have not lecture because of typhoon!");
INSERT INTO `Course` VALUES ("COMP3231", "Computer Architecture", "Dr. Craftman Spencer", "An interesting article about why you should use SSD in 2023: www.crucial.com/sellout","No zoom recording for today, we will have lab session today!");
INSERT INTO `Course` VALUES ("COMP3356", "Robotics", "Mr. Smart guy", "ROS tutorials for beginners: www.youtube.com/ROSninja", "Remember to submit your assignment by this Sunday!");

-- Table structure for table `Enroll`

Create TABLE `Enroll` (
  `student_id` INT NOT NULL,
  `course_id` varchar(10) NOT NULL,
  -- PRIMARY KEY(`student_id, course_id`),
  FOREIGN KEY(`student_id`) REFERENCES Student (`student_id`),
  FOREIGN KEY(`course_id`) REFERENCES Course (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Enroll` VALUES (1, "COMP3278");
INSERT INTO `Enroll` VALUES (1, "COMP2119");
INSERT INTO `Enroll` VALUES (1, "COMP3231");
INSERT INTO `Enroll` VALUES (1, "COMP3356");

-- Table structure for table `Class`

Create TABLE `Class` (
  `class_id` INT NOT NULL,
  `course_id` varchar(10) NOT NULL,
  `class_type` varchar(10) NOT NULL,
  `classroom_address` varchar(10) NOT NULL,
  `zoom_link` varchar(50) NOT NULL,
  `note_link` varchar(150) NOT NULL,
  `duration` INT NOT NULL, -- integer values, 2 for 2*30mins
  `start_datetime` DATETIME NOT NULL,
  -- PRIMARY KEY(`class_id, course_id`),
  FOREIGN KEY(`course_id`) REFERENCES Course (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Class` VALUES (5, "COMP3278", "Lecture", "MWT2", "hku.zoom.us/COMP3278", "onedrive/COMP3278", 4, "2022-11-19 13:30:00");
INSERT INTO `Class` VALUES (6, "COMP2119", "Tutorial", "CYPP2", "hku.zoom.us/COMP2119", "onedrive/COMP2119", 2, "2022-11-20 09:30:00");
INSERT INTO `Class` VALUES (5, "COMP3231", "Lecture", "CYPP2", "hku.zoom.us/COMP3231", "onedrive/COMP3231", 4, "2022-11-20 13:30:00");
-- testing logic
INSERT INTO `Class` VALUES (6, "COMP3356", "Tutorial", "CPD-01", "https://hku.zoom.us/j/5053938647", "https://moodle.hku.hk/course/COMP3356/note6", 2, "2022-11-20 17:30:00"); -- for demonstration when less than 1 hour to lesson
