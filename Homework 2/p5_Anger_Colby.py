import sys
import unittest
from datetime import datetime
from tempfile import NamedTemporaryFile
from unittest.mock import patch


DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MIN_TEMPERATURE = -100.0
MAX_TEMPERATURE = 150.0


def read_observations(filename):
	"""Read valid station observations and return them with line errors."""
	observations = {}
	errors = []
	seen = set()

	with open(filename, "r", encoding="utf-8") as input_file:
		for line_number, line in enumerate(input_file, start=1):
			fields = line.rstrip("\n\r").split(",")
			if len(fields) != 3:
				errors.append((line_number, "Malformed line"))
				continue

			station, date_text, temperature_text = (field.strip() for field in fields)
			if not station or not date_text or not temperature_text:
				errors.append((line_number, "Malformed line"))
				continue

			try:
				date = datetime.strptime(date_text, DATE_FORMAT)
			except ValueError:
				errors.append((line_number, "Malformed line"))
				continue

			try:
				temperature = float(temperature_text)
			except ValueError:
				errors.append((line_number, "Invalid temperature"))
				continue

			if not MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE:
				errors.append((line_number, "Invalid temperature"))
				continue

			observation_key = (station, date)
			if observation_key in seen:
				errors.append((line_number, "Duplicate observation"))
				continue

			seen.add(observation_key)
			observations.setdefault(station, []).append((date, temperature))

	for station in observations:
		observations[station].sort(key=lambda observation: observation[0])

	return observations, errors


def station_statistics(observations):
	"""Return minimum, maximum, and mean temperature for every station."""
	return {
		station: (
			min(temperature for _, temperature in station_observations),
			max(temperature for _, temperature in station_observations),
			sum(temperature for _, temperature in station_observations)
			/ len(station_observations),
		)
		for station, station_observations in observations.items()
	}


def station_outliers(observations):
	"""Return stations whose latest temperature is above their station mean."""
	statistics = station_statistics(observations)
	return {
		station: (latest_date, latest_temperature, statistics[station][2])
		for station, station_observations in observations.items()
		for latest_date, latest_temperature in [station_observations[-1]]
		if latest_temperature > statistics[station][2]
	}


def write_statistics(filename, statistics):
	"""Write station statistics in lexicographic station order."""
	with open(filename, "w", encoding="utf-8") as output_file:
		for station in sorted(statistics):
			minimum, maximum, mean = statistics[station]
			output_file.write(
				f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n"
			)


def main():
	"""Read the command-line files, print results, and write statistics."""
	if len(sys.argv) != 3:
		print("Usage: python p5_Anger_Colby.py input_file output_file")
		return

	input_filename, output_filename = sys.argv[1:]
	try:
		observations, errors = read_observations(input_filename)
		statistics = station_statistics(observations)
		outliers = station_outliers(observations)
		write_statistics(output_filename, statistics)
	except OSError as error:
		print(f"File access error: {error}")
		return

	print("Statistics:")
	for station in sorted(statistics):
		minimum, maximum, mean = statistics[station]
		print(f"{station}: min={minimum:.1f}, max={maximum:.1f}, mean={mean:.1f}")

	print("Outliers:")
	for station in sorted(outliers):
		date, temperature, mean = outliers[station]
		print(f"{station}: {date.strftime(DATE_FORMAT)}, {temperature:.1f}, {mean:.1f}")

	if errors:
		print("Errors:")
		for line_number, error_message in errors:
			print(f"line {line_number}: {error_message}")


class TestTemperatureAnalysis(unittest.TestCase):
	def create_input_file(self, contents):
		input_file = NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
		input_file.write(contents)
		input_file.close()
		self.addCleanup(lambda: self.remove_file(input_file.name))
		return input_file.name

	@staticmethod
	def remove_file(filename):
		import os

		if os.path.exists(filename):
			os.remove(filename)

	def test_reads_several_stations_and_sorts_observations(self):
		filename = self.create_input_file(
			"Beta,09:28:09 AM 04/20/2026,70\n"
			"Alpha,09:28:09 AM 04/19/2026,60\n"
			"Beta,09:28:09 AM 04/19/2026,65\n"
		)
		observations, errors = read_observations(filename)
		self.assertEqual(errors, [])
		self.assertEqual(list(observations), ["Beta", "Alpha"])
		self.assertLess(observations["Beta"][0][0], observations["Beta"][1][0])

	def test_accepts_negative_temperatures(self):
		filename = self.create_input_file("North,09:28:09 AM 04/20/2026,-40.5\n")
		observations, errors = read_observations(filename)
		self.assertEqual(errors, [])
		self.assertEqual(observations["North"][0][1], -40.5)

	def test_rejects_duplicate_observations(self):
		filename = self.create_input_file(
			"North,09:28:09 AM 04/20/2026,40\n"
			"North,09:28:09 AM 04/20/2026,41\n"
		)
		observations, errors = read_observations(filename)
		self.assertEqual(len(observations["North"]), 1)
		self.assertEqual(errors, [(2, "Duplicate observation")])

	def test_rejects_invalid_temperature_ranges(self):
		filename = self.create_input_file(
			"A,09:28:09 AM 04/20/2026,-100.1\n"
			"B,09:28:09 AM 04/20/2026,150.1\n"
		)
		observations, errors = read_observations(filename)
		self.assertEqual(observations, {})
		self.assertEqual(errors, [(1, "Invalid temperature"), (2, "Invalid temperature")])

	def test_calculates_statistics_and_outliers(self):
		observations = {
			"A": [
				(datetime(2026, 4, 19, 9, 28, 9), 10.0),
				(datetime(2026, 4, 20, 9, 28, 9), 20.0),
			],
			"B": [(datetime(2026, 4, 20, 9, 28, 9), -5.0)],
		}
		self.assertEqual(station_statistics(observations), {"A": (10.0, 20.0, 15.0), "B": (-5.0, -5.0, -5.0)})
		self.assertEqual(station_outliers(observations)["A"][1:], (20.0, 15.0))

	def test_writes_sorted_statistics_with_one_decimal(self):
		filename = self.create_input_file("")
		write_statistics(filename, {"Zoo": (1, 4, 2.5), "Alpha": (-2, 3, 0.5)})
		with open(filename, "r", encoding="utf-8") as output_file:
			self.assertEqual(output_file.read(), "Alpha,-2.0,3.0,0.5\nZoo,1.0,4.0,2.5\n")

	def test_missing_file_raises_file_not_found_error(self):
		with self.assertRaises(FileNotFoundError):
			read_observations("missing-temperature-file.csv")


if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] in {"-m", "--test"}:
		sys.argv.pop(1)
		unittest.main()
	else:
		main()
