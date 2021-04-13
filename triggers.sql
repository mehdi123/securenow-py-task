CREATE DEFINER = CURRENT_USER TRIGGER `mydb`.`Booking_BEFORE_INSERT` BEFORE INSERT ON `Booking` FOR EACH ROW
BEGIN
	if ABS(DATEDIFF(NEW.data_of_hire, NEW.date_of_return)) > 7 THEN
		signal sqlstate '45000';
    END if;
    if DATEDIFF(NEW.date_of_hire, NOW()) > 7 THEN
		signal sqlstate '45000';
	END if;
    if NEW.vehicle_id in ( /* Check car availabilty */
		SELECT B.vehicle_id 
        FROM Booking B 
        WHERE ( NEW.vehicle_id == B.vehicle_id and B.returned == 0)
    ) THEN
		signal sqlstate '45000';
	END if;
END