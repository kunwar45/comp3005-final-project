INSERT INTO subscription (tier_name, description, price) VALUES 
    ('Bronze', 'Access to gym equipment and classes', 10.00),
    ('Silver', 'Access to gym equipment and classes, pool and sauna', 20.00),
    ('Gold', 'Access to all facilities, towel service, and exclusive events', 30.00);

INSERT INTO member (name, subscription_id) VALUES 
    ('John Adams', (SELECT subscription_id FROM subscription WHERE tier_name = 'Bronze')),
    ('May First', (SELECT subscription_id FROM subscription WHERE tier_name = 'Bronze')),
    ('Allen Sam', (SELECT subscription_id FROM subscription WHERE tier_name = 'Silver')),
    ('Sarah We', (SELECT subscription_id FROM subscription WHERE tier_name = 'Gold'));

INSERT INTO metrics (member_id, weight, height, age) VALUES
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 70, 175, 30),
    ((SELECT member_id FROM member WHERE name = 'May First'), 60, 165, 25),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 80, 180, 35),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), 55, 160, 28);

INSERT INTO goal (member_id, description, date_completed) VALUES
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Run 10K', NULL),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Bench 225', NULL),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Swim 4K', NULL);

INSERT INTO employee (name) VALUES 
    ('Sam Sulek'),
    ('Austin Pham'),
    ('Matt Stark');

INSERT INTO trainer (employee_id) VALUES
    ((SELECT employee_id FROM employee WHERE name = 'Sam Sulek')),
    ((SELECT employee_id FROM employee WHERE name = 'Matt Stark'));

INSERT INTO admin (employee_id) VALUES 
    ((SELECT employee_id FROM employee WHERE name = 'Austin Pham'));

-- Inserting classes with details matching the provided available times
INSERT INTO class (class_name, start_time, end_time, date, purpose, description, trainer_id, max_attendance, current_num_attendees) VALUES 
    ('Personal Yoga', '14:00:00', '16:00:00', '2024-04-16', 'Flexibility', 'Solo Yoga Session focusing on flexibility and core strength.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark'), 1, 0),
    ('Personal Kickboxing', '11:00:00', '13:00:00', '2024-04-13', 'Self-Defence', 'Solo defence Session.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek'), 1, 0),
    ('Yoga', '11:00:00', '13:00:00', '2024-04-13', 'Flexibility', 'Group Yoga Session focusing on flexibility and core strength.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek'), 20, 0),
    ('High-Intensity Interval Training', '16:00:00', '18:00:00', '2024-05-01', 'Fitness', 'High-paced interval training to boost cardiovascular health and stamina.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek'), 15, 0),
    ('Strength Training', '14:00:00', '16:00:00', '2024-05-04', 'Muscle Building', 'Comprehensive strength training session focusing on major muscle groups.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek'), 12, 0),
    ('Cardio Kickboxing', '11:00:00', '13:00:00', '2024-04-24', 'Cardio', 'Energetic kickboxing class that improves flexibility, strength, and cardiovascular endurance.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark'), 18, 0),
    ('Circuit Training', '09:00:00', '11:00:00', '2024-04-15', 'Fitness', 'Circuit Training involving a series of exercises targeting different muscle groups with minimal rest.', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark'), 10, 0);

INSERT INTO room (room_number, name, description) VALUES
    (101, 'Ravens Nest', 'Indoor track and soccer field'),
    (102, 'Yoga Room', 'Open spacious fitness room with free weights and mats.'),
    (103, 'Gym', 'Modern fitness room featuring state-of-the-art equipment and exercise stations.');

INSERT INTO exercise_routine (member_id, description) VALUES 
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Circuit training: 5 rounds of push-ups, sit-ups, and squats'),
    ((SELECT member_id FROM member WHERE name = 'May First'), 'Circuit training: 5 rounds of push-ups, sit-ups, and squats'),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Swim for 30 minutes followed by 15 minutes of yoga'),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), '3 sets of 12 reps bench press, 3 sets of 10 reps squat'),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), '30 minutes of high-intensity interval training'),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), '2 hours of mixed martial arts training'),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Circuit training: 5 rounds of push-ups, sit-ups, and squats'),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Circuit training: 5 rounds of push-ups, sit-ups, and squats'),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Swim for 30 minutes followed by 15 minutes of yoga'),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), '30 minutes of high-intensity interval training');

INSERT INTO available_time (date, start_time, end_time, trainer_id) VALUES 
    ('2024-04-13', '11:00:00', '13:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek')),
    ('2024-05-01', '16:00:00', '18:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek')),
    ('2024-05-04', '14:00:00', '16:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek')),
    ('2024-04-24', '11:00:00', '13:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark')),
    ('2024-04-15', '09:00:00', '11:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark')),
    ('2024-04-22', '16:00:00', '18:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek')),
    ('2024-05-09', '09:00:00', '11:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark')),
    ('2024-05-01', '09:00:00', '11:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark')),
    ('2024-04-16', '14:00:00', '16:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Matt Stark')),
    ('2024-05-07', '14:00:00', '16:00:00', (SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = 'Sam Sulek'));

INSERT INTO takes (member_id, class_id) VALUES 
    ((SELECT member_id FROM member WHERE name = 'John Adams'), (SELECT class_id FROM class WHERE class_name = 'Yoga')),
    ((SELECT member_id FROM member WHERE name = 'May First'), (SELECT class_id FROM class WHERE class_name = 'Yoga')),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), (SELECT class_id FROM class WHERE class_name = 'Cardio Kickboxing')),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), (SELECT class_id FROM class WHERE class_name = 'Yoga')),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), (SELECT class_id FROM class WHERE class_name = 'Cardio Kickboxing'));

INSERT INTO booking (class_id, room_id) VALUES 
    ((SELECT class_id FROM class WHERE class_name = 'Yoga'), (SELECT room_id FROM room WHERE name = 'Yoga Room')),
    ((SELECT class_id FROM class WHERE class_name = 'Cardio Kickboxing'), (SELECT room_id FROM room WHERE name = 'Ravens Nest')),
    ((SELECT class_id FROM class WHERE class_name = 'Strength Training'), (SELECT room_id FROM room WHERE name = 'Gym'));

INSERT INTO equipment (name, room_id, description, last_serviced) VALUES 
    ('Treadmill', (SELECT room_id FROM room WHERE name = 'Ravens Nest'), 'Treadmill for cardio workouts.', '2023-04-26'),
    ('Elliptical', (SELECT room_id FROM room WHERE name = 'Ravens Nest'), 'Elliptical for low-impact cardio.', '2023-09-06');
    
INSERT INTO equipment (name, room_id, description, last_serviced) VALUES 
    ('Yoga Mat', (SELECT room_id FROM room WHERE name = 'Yoga Room'), 'Yoga Mat for yoga sessions.', '2024-04-02'),
    ('Foam Roller', (SELECT room_id FROM room WHERE name = 'Yoga Room'), 'Foam Roller for muscle relaxation.', '2023-12-23');

INSERT INTO equipment (name, room_id, description, last_serviced) VALUES 
    ('Dumbbell', (SELECT room_id FROM room WHERE name = 'Gym'), 'Dumbbells for strength training.', '2023-07-17'),
    ('Squat Rack', (SELECT room_id FROM room WHERE name = 'Gym'), 'Squat Rack for squats and lifts.', '2023-08-02');

INSERT INTO billing (member_id, date_billed, payed) VALUES 
    ((SELECT member_id FROM member WHERE name = 'John Adams'), '2024-01-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), '2024-02-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), '2024-03-01', TRUE),
    
    ((SELECT member_id FROM member WHERE name = 'May First'), '2024-01-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'May First'), '2024-02-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'May First'), '2024-03-01', FALSE),
    
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), '2024-01-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), '2024-02-01', FALSE),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), '2024-03-01', FALSE),
    
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), '2024-01-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), '2024-02-01', TRUE),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), '2024-03-01', TRUE);

INSERT INTO goal (member_id, description, date_completed) VALUES
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Run 10K', '2024-03-15'),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Bench 225', NULL),
    ((SELECT member_id FROM member WHERE name = 'John Adams'), 'Swim 4K', '2010-01-15'),

    ((SELECT member_id FROM member WHERE name = 'May First'), 'Lose 5 pounds', NULL),
    ((SELECT member_id FROM member WHERE name = 'May First'), 'Increase flexibility', '2012-06-20'),

    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Complete 10 consecutive pull-ups', NULL),
    ((SELECT member_id FROM member WHERE name = 'Allen Sam'), 'Run a half-marathon', '2013-02-20'),

    ((SELECT member_id FROM member WHERE name = 'Sarah We'), 'Achieve bodyweight squat 1RM', NULL),
    ((SELECT member_id FROM member WHERE name = 'Sarah We'), 'Improve deadlift form', NULL);
