from io import StringIO
import csv


@app.route("/export_csv", methods=["POST"])
def export_data():
  # Connect to MySQL database
    cursor = db.connection.cursor()
    # Data de equipos
    cursor.execute("SELECT * FROM equipos WHERE id_user = %s", (session["user_id"],))
    equipos = cursor.fetchall()    
    # Data de hardware
    cursor.execute("SELECT * FROM hardware WHERE id_equipo IS NULL AND id_user = %s", (session["user_id"],))
    hardware = cursor.fetchall()

    # Prepare data for CSV (more on this in step 2)
    csv_data = prepare_csv_data(equipos, hardware)

    return send_csv_response(csv_data)


def prepare_csv_data(equipos, hardware):
  csv_content = []

  # Equipos table header
  equipos_header = []
  for key, value in equipos[0]:
     equipos_header.append(str(key))
  csv_content.append(equipos_header)
  csv_content.extend(equipos)  # Add equipos data rows

  # Empty row separator
  csv_content.append([])

  # Software table header
  hw_header = []
  for key, value in hardware[0]:
     hw_header.append(str(key))
  csv_content.append(hw_header)
  csv_content.extend(hardware)  # Add software data rows

  return csv_content


def send_csv_response(csv_data):
  # Create a StringIO object to hold the CSV data
  csv_buffer = StringIO()
  writer = csv.writer(csv_buffer)

  # Write the data to the buffer
  writer.writerows(csv_data)

  # Set response headers
  response = make_response(csv_buffer.getvalue())
  response.headers["Content-Disposition"] = "attachment;filename=hardware_software.csv"
  response.headers["Content-Type"] = "text/csv"

  return response