import { exec } from 'child_process';
import { NextApiRequest, NextApiResponse } from 'next';
import Database from 'better-sqlite3';
import axios from 'axios';


export default async function handler(req: NextApiRequest, res: NextApiResponse) {

  const runPythonScript = (scriptPath: string, args: string[]): Promise<string> => {
    return new Promise((resolve, reject) => {
      const command = `python ${scriptPath} ${args.join(' ')}`;
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script: ${error.message}`);
          reject(error);
        } else if (stderr) {
          console.error(`Python script returned an error: ${stderr}`);
          reject(new Error(stderr));
        } else {
          resolve(stdout);
        }
      });
    });
  };

  try {
    const { lat, lon, year, month, day, meanTemp, meanRain, meanSnow, ecoZone } = req.query;


    if (!lat || !lon || !year || !month || !day || !meanTemp || !meanRain || !meanSnow || !ecoZone) {
      throw new Error('Invalid arguments');
    }

    if (typeof lat != 'string' || typeof lon != 'string' || typeof year != 'string' || typeof month != 'string' || typeof day != 'string' || typeof meanTemp != 'string' || typeof meanRain != 'string' || typeof meanSnow != 'string' || typeof ecoZone != 'string') {
      throw new Error("Invalid arguments");
    }

    if (parseFloat(lat) === 0 || parseFloat(lon) === 0) {
      throw new Error('Invalid arguments');
    }

    const url = `https://flask-hello-world-laijackylai-laijackylai-pro.vercel.app/pred?lat=${lat}&lon=${lon}&year=${year}&month=${month}&day=${day}&meanTemp=${meanTemp}&meanRain=${meanRain}&meanSnow=${meanSnow}&ecoZone=${ecoZone}`;
    const response = await axios.get(url);

    console.log(response)

    if (response) {
      res.status(200).json({
        "result": 'success',
        "data": response.data
      });
    } else {
      res.status(400).json({
        "result": 'failed',
        "data": []
      });
    }

    // * old python way
    // const args = ["--lat", lat, "--lon", lon, "--year", year, "--month", month, "--day", day, "--meanTemp", meanTemp, "--meanRain", meanRain, "--meanSnow", meanSnow, "--ecoZone", ecoZone]

    // const scriptPath = 'ml/pred.py';
    // const result = await runPythonScript(scriptPath, args);

    // if (result.trim() === 'success') {
    //   const dbOptions = {
    //     fileMustExist: true,
    //     // verbose: console.log
    //   }
    //   const db = new Database('./ml/pred.db', dbOptions);
    //   db.pragma('journal_mode = WAL');

    //   const stmt = db.prepare('SELECT * FROM pred')
    //   const rows = stmt.all();

    //   res.status(200).json({
    //     "result": result,
    //     "data": rows
    //   });

    //   db.close()
    // } else {
    //   res.status(400).json({
    //     "result": result,
    //     "data": []
    //   });
    // }
  } catch (error) {
    console.error('Error running Python script:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      msg: error
    });
  }
}