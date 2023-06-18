import { exec } from 'child_process';
import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import Database from 'better-sqlite3';



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
    const { strategy, query } = req.query;

    if (!strategy || !query) {
      throw new Error('Invalid arguments');
    }

    if (typeof strategy != 'string' || typeof query != 'string') {
      throw new Error("Invalid arguments");
    }

    const encodedQuery = encodeURIComponent(query.replace(/"/g, ''));
    const url = `https://flask-hello-world-laijackylai-laijackylai-pro.vercel.app/data?strategy=${strategy.replace(/"/g, '')}&query=${encodedQuery}`;
    const response = await axios.get(url);

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
    // const args = ["--strategy", strategy, "--query", query]

    // const scriptPath = 'ml/nlp_search.py';
    // const result = await runPythonScript(scriptPath, args);

    // if (result.trim() === 'success') {
    //   const dbOptions = {
    //     fileMustExist: true,
    //     // verbose: console.log
    //   }
    //   const db = new Database('./ml/query.db', dbOptions);
    //   db.pragma('journal_mode = WAL');

    //   const stmt = db.prepare('SELECT * FROM query')
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
    console.error('Error:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      msg: error
    });
  }
}