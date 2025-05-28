import unittest
import os
import string
import secrets
import tempfile
import shutil # For cleaning up directories

# Make sure the script can find cop_pass.py, especially if tests are run from a different directory
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Add current dir to path

from cop_pass import generate_password_and_save, _secure_shuffle


class TestSecureShuffle(unittest.TestCase):
    def test_shuffle_maintains_elements(self):
        """Test that shuffling doesn't add or remove elements."""
        original_list = list(range(100))
        shuffled_list = original_list[:]  # Create a copy
        _secure_shuffle(shuffled_list)
        self.assertEqual(len(original_list), len(shuffled_list), "Length of list changed after shuffle.")
        self.assertEqual(sorted(original_list), sorted(shuffled_list), "Elements in list changed after shuffle.")

    def test_shuffle_changes_order(self):
        """Test that shuffling usually changes the order of elements."""
        # This test is probabilistic. For a small list, it's possible (though unlikely)
        # for the shuffled list to be identical to the original.
        # For a list of 100 elements, the probability of it remaining unchanged is astronomically small (1/100!).
        original_list = list(range(100))
        # To be absolutely sure secrets.randbelow is being used, we can't just check if the list is different.
        # Instead, we'll run it a few times and check if it's *ever* different.
        # A more robust test would involve mocking secrets.randbelow, but that's more complex.
        
        attempts = 5
        changed_at_least_once = False
        for _ in range(attempts):
            shuffled_list = original_list[:]
            _secure_shuffle(shuffled_list)
            if shuffled_list != original_list:
                changed_at_least_once = True
                break
        
        # If the list is very small (e.g., 1 or 2 elements), it might not change order frequently.
        # However, for a list of 100, it should definitely change.
        if len(original_list) > 2: # Only assert change if the list is long enough to expect a change
            self.assertTrue(changed_at_least_once, 
                            f"Order of list with {len(original_list)} elements did not change after {attempts} shuffles. "
                            "This is highly unlikely if _secure_shuffle is working correctly.")
        else:
            # For very short lists, we just ensure it runs without error
            self.assertEqual(sorted(original_list), sorted(shuffled_list))


class TestGeneratePasswordAndSave(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        # Construct a file path within the temporary directory
        self.test_file = os.path.join(self.test_dir, "test_pass.txt")

    def tearDown(self):
        """Remove the temporary directory and its contents after tests."""
        shutil.rmtree(self.test_dir)

    def _verify_password_chars(self, password, min_lower, min_upper, min_digits, min_punctuation):
        """Helper function to verify character counts in the password."""
        self.assertTrue(sum(c.islower() for c in password) >= min_lower, f"Password '{password}' has too few lowercase chars.")
        self.assertTrue(sum(c.isupper() for c in password) >= min_upper, f"Password '{password}' has too few uppercase chars.")
        self.assertTrue(sum(c.isdigit() for c in password) >= min_digits, f"Password '{password}' has too few digits.")
        self.assertTrue(sum(c in string.punctuation for c in password) >= min_punctuation, f"Password '{password}' has too few punctuation chars.")

    def test_default_parameters(self):
        """Test password generation with default parameters."""
        # Default parameters from cop_pass.py: length=8, min_lower=1, min_upper=1, min_digits=3, min_punctuation=1
        # So, required_char_count = 1+1+3+1 = 6. Default length 8 is fine.
        expected_length = 8
        min_l, min_u, min_d, min_p = 1, 1, 3, 1
        
        password = generate_password_and_save(file_name=self.test_file) # Uses default length
        self.assertEqual(len(password), expected_length, "Password length is not the default.")
        self._verify_password_chars(password, min_l, min_u, min_d, min_p)
        
        self.assertTrue(os.path.exists(self.test_file), "Password file was not created.")
        with open(self.test_file, "r") as f:
            content = f.read().strip()
            self.assertEqual(content, password, "Password in file does not match generated password.")

    def test_custom_parameters(self):
        """Test with custom length and character minimums."""
        custom_length = 16
        min_l, min_u, min_d, min_p = 2, 2, 4, 2
        password = generate_password_and_save(length=custom_length, 
                                              file_name=self.test_file,
                                              min_lower=min_l, 
                                              min_upper=min_u, 
                                              min_digits=min_d, 
                                              min_punctuation=min_p)
        self.assertEqual(len(password), custom_length)
        self._verify_password_chars(password, min_l, min_u, min_d, min_p)
        self.assertTrue(os.path.exists(self.test_file))

    def test_all_characters_used_when_length_is_minimum(self):
        """Test that if length equals required_char_count, password has exact minimums."""
        min_l, min_u, min_d, min_p = 1, 1, 1, 1
        required_length = min_l + min_u + min_d + min_p # Should be 4
        
        password = generate_password_and_save(length=required_length,
                                              file_name=self.test_file,
                                              min_lower=min_l,
                                              min_upper=min_u,
                                              min_digits=min_d,
                                              min_punctuation=min_p)
        self.assertEqual(len(password), required_length)
        # Check exact counts, not just >=
        self.assertEqual(sum(c.islower() for c in password), min_l, "Exact min_lower not met.")
        self.assertEqual(sum(c.isupper() for c in password), min_u, "Exact min_upper not met.")
        self.assertEqual(sum(c.isdigit() for c in password), min_d, "Exact min_digits not met.")
        self.assertEqual(sum(c in string.punctuation for c in password), min_p, "Exact min_punctuation not met.")

    def test_min_lower_respected(self):
        password = generate_password_and_save(length=10, min_lower=5, file_name=self.test_file)
        self._verify_password_chars(password, 5, 1, 1, 1) # Default other minimums

    def test_min_upper_respected(self):
        password = generate_password_and_save(length=10, min_upper=5, file_name=self.test_file)
        self._verify_password_chars(password, 1, 5, 1, 1)

    def test_min_digits_respected(self):
        # Default min_digits is 3, so let's test a higher value
        password = generate_password_and_save(length=10, min_digits=5, file_name=self.test_file)
        self._verify_password_chars(password, 1, 1, 5, 1)

    def test_min_punctuation_respected(self):
        password = generate_password_and_save(length=10, min_punctuation=4, file_name=self.test_file)
        self._verify_password_chars(password, 1, 1, 1, 4) # Default min_digits is 3, but we are testing punctuation

    def test_length_too_short_error(self):
        """Test ValueError for insufficient length."""
        # Default minimums: lower=1, upper=1, digits=3, punctuation=1. Total = 6
        with self.assertRaisesRegex(ValueError, "La longitud de la contraseña \(5\) es demasiado corta. Se requiere una longitud mínima de 6"):
            generate_password_and_save(length=5, file_name=self.test_file)

        with self.assertRaisesRegex(ValueError, "La longitud de la contraseña \(10\) es demasiado corta. Se requiere una longitud mínima de 11"):
            generate_password_and_save(length=10, min_lower=3, min_upper=3, min_digits=3, min_punctuation=2, file_name=self.test_file) # 3+3+3+2 = 11

    def test_file_creation_and_content(self):
        """Test password file creation and content."""
        password = generate_password_and_save(length=12, file_name=self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, "r") as f:
            content = f.read().strip() # .strip() to remove the newline
            self.assertEqual(content, password)

    def test_directory_creation(self):
        """Test that the target directory is created if it doesn't exist."""
        # Create a path for a subdirectory within the temp_dir
        nested_dir = os.path.join(self.test_dir, "sub_dir")
        nested_file = os.path.join(nested_dir, "another_pass.txt")
        
        self.assertFalse(os.path.exists(nested_dir), "Nested directory already exists before test.")
        
        generate_password_and_save(length=12, file_name=nested_file)
        
        self.assertTrue(os.path.exists(nested_dir), "Nested directory was not created.")
        self.assertTrue(os.path.exists(nested_file), "Password file in nested directory was not created.")

    def test_file_append(self):
        """Test that passwords are appended to an existing file."""
        password_1 = generate_password_and_save(length=10, file_name=self.test_file)
        password_2 = generate_password_and_save(length=11, file_name=self.test_file)
        
        with open(self.test_file, "r") as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 2, "Not enough passwords in the file.")
        self.assertEqual(lines[0].strip(), password_1)
        self.assertEqual(lines[1].strip(), password_2)

if __name__ == '__main__':
    unittest.main()
