import { LogLevel, LoggerRegistry } from "@jupyterlab/logconsole"
import { 
    RenderMimeRegistry,
    standardRendererFactories as initialFactories 
  } from '@jupyterlab/rendermime';

declare const DEFAULT_LOGGING_LEVEL: LogLevel

export class Logger {
    logger_registry: LoggerRegistry = new LoggerRegistry({
        defaultRendermime: new RenderMimeRegistry({ initialFactories }),
        maxLength: 1000
    })
    name: "jupyterlab-requirements"

}
