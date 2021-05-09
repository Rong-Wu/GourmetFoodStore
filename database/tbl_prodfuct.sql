-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 07, 2021 at 08:49 PM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `GourmetFood`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_product`
--

CREATE TABLE `tbl_product` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` text NOT NULL,
  `inventory` int(11) NOT NULL DEFAULT '15',
  `price` int(11) NOT NULL,
  `picture_url` varchar(100) NOT NULL,
  `category_id` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tbl_product`
--

INSERT INTO `tbl_product` (`id`, `name`, `description`, `inventory`, `price`, `picture_url`, `category_id`) VALUES
(1, 'Guava Strudel', 'A crispy and flaky puff pastry filled with guava puree and cream cheese then topped with crystal sugar', 15, 5, 'static/img/1.jpg', 1),
(2, 'Chocolate Croissants', 'crispy and flaky chocolate croissant', 15, 6, 'static/img/2.jpg', 1),
(3, 'Croissant butter mini', 'Wheat Flour, Butter (cream, water), Water, Sugar, Yeast, Whole Eggs, Salt, Wheat Gluten, Malted Wheat Flour (malted wheat), Deactivated Yeast, Ascorbic Acid, Enzymes', 15, 5, 'static/img/3.jpg', 1),
(4, 'Pastry turnover apple', 'Apple Filling (apples, sugar, water, corn starch, cinnamon, ascorbic acid, citric acid), Enriched Wheat Flour (flour, niacin, reduced iron, thiamine mononitrate, riboflavin, ascorbic acid, folic acid, enzymes), Margarine (palm oil, water, canola oil, vinegar, sugar, canola and/or soy lecithin, natural flavor, annatto color, vitamin a palmitate, vitamin d3), Water, Sugar, Salt.', 15, 7, 'static/img/4.jpg', 1),
(5, 'Bread rye old world', 'Bread (unbleached wheat flour [wheat flour, malted barley flour], filtered water, whole rye flour, caraway seeds, sea salt, vital wheat gluten, yeast, ascorbic acid).', 15, 5, 'static/img/5.jpg', 1),
(6, 'Slow Dough Pugliese Bread', 'Unbleached Unbromated Enriched Artisan Bread Flour (wheat flour, malted barley flour, niacin, iron [reduced], thiamine mononitrate, riboflavin, folic acid), Water, Sea Salt, Dry Malt (malted barley flour, wheat flour, dextrose), Yeast.', 15, 8, 'static/img/6.jpg', 1),
(7, 'Chocolate Chip Cookie', 'All the goodness of chocolate chips blended into our chewy delicious cookie', 15, 4, 'static/img/7.jpg', 2),
(8, 'Blueberry scone', 'Unbleached Enriched Wheat Flour (wheat flour, niacin, iron, ascorbic acid, thiamine, riboflavin, amylase, folic acid), Butter (100 % cream), Water, Cane Sugar, Frozen Wild Blueberries, Skim Milk Powder, Baking Powder (sodium acid pyrophosphate, sodium bicarbonate, corn starch, monocalcium phosphate monohydrate, calcium sulfate), Canola Oil, Sea Salt (sea salt, sodium ferrocyanide).', 15, 6, 'static/img/8.jpg', 2),
(9, 'Chocolate chip scone', 'Unbleached Enriched Wheat Flour (wheat flour, niacin, iron, ascorbic acid, thiamine, riboflavin, amylase, folic acid), Butter (100 % cream), Water, Chocolate Chips (cane sugar, unsweetened chocolate, cocoa butter), Cane Sugar, Skim Milk Powder, Baking Powder (sodium acid pyrophosphate, sodium bicarbonate, corn starch, monocalcium phosphate monohydrate, calcium sulfate), Canola Oil, Sea Salt (sea salt, sodium ferrocyanide).', 15, 7, 'static/img/9.jpg', 2),
(10, 'Brown Sugar Rice Cake', 'Contains brown sugar, glutinous rice, vegetable oil.', 15, 6, 'static/img/10.jpg', 3),
(11, 'Pineapple cake', 'Contains pineapple, rice, flour, vegetable oil', 15, 7, 'static/img/11.jpg', 3),
(12, 'Apricot rice cake', 'Contains apricot, rice, flour, vegetable oil', 15, 5, 'static/img/12.jpg', 3),
(13, 'Ludagun Pastry', 'Beijing traditional gourmet, contain glutinous rice, soybean power, red bean paste.', 15, 7, 'static/img/13.jpg', 3),
(14, 'Lanhuadou', 'Made by broad-bean, sugar, salt ', 15, 5, 'static/img/14.jpg', 4),
(15, 'Haw roll', 'Made by haw and sugar', 15, 4, 'static/img/15.jpg', 4),
(16, 'Zishu Peanut', 'Made by Peanut, purple sweet potato, sugar', 15, 6, 'static/img/16.jpg', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_product`
--
ALTER TABLE `tbl_product`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_product`
--
ALTER TABLE `tbl_product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
