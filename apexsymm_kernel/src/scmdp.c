#include <scmdp.h>

/**
 * @brief Issues an error if something went wrong during the parsing
 * 
 * @param workspace Initialized workspace pointer
 * @param errorCode The code of occured error (see 'enum errors' in scmdp.h file)
 * 
 * @returns Nothing
*/
void _ShowError(ScmdpWorkspace *workspace, int errorCode)
{
    char *error = "";
    switch (errorCode)
    {
    case ERR_NO_VAL_NOPT_PARAMETER:
        error = "Error: Need a value for non-optional parameter!";
        break;
    case ERR_NO_VAL_OPT_PARAMETER:
        error = "Error: Need a value for optional parameter!";
        break;
    case ERR_UNKNOWN_PARAMETER:
        error = "Error: Unknown argument or option!";
        break;
    case ERR_WRONG_PARS_NUMBER:
        error = "Error: Wrong number of parameters!";
        break;
    case ERR_WRONG_SYNTAX:
        error = "Error: Wrong command line syntax!";
        break;
    default:
        break;
    }
    printf("%s\nprint -h or --help to see help\n", error);
}

/**
 * @brief Assemble and show the help for all initialized arguments.
 * The assembly comes from the descriptions entered during initialization of the arguments and the workspace
 * 
 * @warning All error messages and formatting are in this function
 * 
 * @param workspace Initialized workspace pointer
 * @param showFullHelp Checks if full help should be shown or only syntax help
 * 
 * @return Nothing
 */
void _ShowHelp(ScmdpWorkspace *workspace, bool showFullHelp)
{
    char checkSymbol = 0;
    if(!showFullHelp)
    {
        printf("%s\n", workspace->syntaxHelp);
    }
    else
    {
        printf("%s\n\n%s\n", workspace->syntaxHelp, workspace->descriptHelp);
        
        printf("\n>> Non-optional arguments:\n");
        for (int i = 0; i < workspace->numOfNonOptArgs; i++)
        {
            printf("\n%3s%-10s", " ", workspace->nonOptArgs[i].key);
            for (int j = 0; j < strlen(workspace->nonOptArgs[i].help); j++)
            {
                checkSymbol = workspace->nonOptArgs[i].help[j];
                if (checkSymbol == '\n')
                {
                    printf("\n%-13s", " ");
                }
                else
                {
                    printf("%c", checkSymbol);
                }
            }
        }
        printf("\n\n>> Optional agruments:\n");
        for (int i = 0; i < workspace->numOfOptArgs; i++)
        {
            printf("\n%3s%-10s,%-5s%-7s", " ", workspace->optArgs[i].longKey, workspace->optArgs[i].shortKey, workspace->optArgs[i].valName);
            for (int j = 0; j < strlen(workspace->optArgs[i].help); j++)
            {
                checkSymbol = workspace->optArgs[i].help[j];
                if (checkSymbol == '\n')
                {
                    printf("\n%-26s", " ");
                }
                else
                {
                    printf("%c", checkSymbol);
                }
            }
        }
    }
}

/** 
 * @brief Remove the whole workspace with all initialized arguments from memory
 * 
 * @warning By default this function is called automatically when  function parsearg() ends
 * 
 * @param workspace Initialized workspace pointer
 * 
 * @returns Nothing
 */
void _DeleteWorkspace(ScmdpWorkspace *workspace)
{
    free(workspace->optArgs);
    free(workspace->nonOptArgs);
}

ScmdpWorkspace AddWorkspace(const char *syntaxHelp, const char *description)
{
    ScmdpWorkspace newWorkspace;

    newWorkspace.optArgs = (ScmdpOptArg*)malloc(sizeof(ScmdpOptArg));
    newWorkspace.nonOptArgs = (ScmdpNonOptArg*)malloc(sizeof(ScmdpNonOptArg));

    newWorkspace.numOfNonOptArgs = 0;
    newWorkspace.numOfOptArgs = 0;
    newWorkspace.numOfValOptArgs = 0;

    newWorkspace.helpArg.longHelpKey = "";
    newWorkspace.helpArg.shortHelpKey = "";

    newWorkspace.syntaxHelp = syntaxHelp;
    newWorkspace.descriptHelp = description;

    return newWorkspace;
}

void AddHelpArg(ScmdpWorkspace *workspace, const char *longKey, const char *shortKey)
{
    ScmdpHelpArg newHelpArg;

    newHelpArg.longHelpKey = longKey;
    newHelpArg.shortHelpKey = shortKey;
    
    workspace->helpArg = newHelpArg;
}

void AddOptArg(ScmdpWorkspace *workspace, const char *longKey, const char *shortKey, const char *help, const char *valName, const char **valPlace)
{
    ScmdpOptArg newOptArg;

    newOptArg.longKey = longKey;
    newOptArg.shortKey = shortKey;
    newOptArg.help = help;
    newOptArg.valPlace = valPlace;
    newOptArg.valName = valName;

    if (strcmp(valName, "") != 0 && valName != NULL)
    {
        workspace->numOfValOptArgs += 1;
        newOptArg.isValuable = true;
    }
    else
    {
        newOptArg.isValuable = false;
    }

    workspace->numOfOptArgs += 1;
    workspace->optArgs = (ScmdpOptArg*)realloc(workspace->optArgs, sizeof(ScmdpOptArg) * workspace->numOfOptArgs);
    workspace->optArgs[workspace->numOfOptArgs-1] = newOptArg;
}

void AddNonOptArg(ScmdpWorkspace *workspace, const char *key, const char *help, const char **valPlace)
{
    ScmdpNonOptArg newNonOptArg;

    newNonOptArg.key = key;
    newNonOptArg.help = help;
    newNonOptArg.valPlace = valPlace;

    workspace->numOfNonOptArgs += 1;
    workspace->nonOptArgs = (ScmdpNonOptArg*)realloc(workspace->nonOptArgs, sizeof(ScmdpNonOptArg) * workspace->numOfNonOptArgs);
    workspace->nonOptArgs[workspace->numOfNonOptArgs-1] = newNonOptArg;
}

bool _IsHelpKeyPresents(ScmdpWorkspace *workspace, int argc, const char *argv[])
{
    bool presents = false;

    for (int i = 1; i < argc; i++)
    {
        if(strcmp(argv[i], workspace->helpArg.longHelpKey) == 0 || strcmp(argv[i], workspace->helpArg.shortHelpKey) == 0)
        {
            presents = true;
            break;
        }
    }

    return presents;
}

bool _IsOptArgKeyExists(ScmdpWorkspace *workspace, const char* key)
{
    bool exists = false;
    for (int i = 0; i < workspace->numOfOptArgs; i++)
    {
        if(strcmp(workspace->optArgs[i].longKey, key) == 0 || strcmp(workspace->optArgs[i].shortKey, key) == 0)
        {
            exists = true;
            break;
        }
    }
    return exists;
}

bool _IsNotAKey(const char* arg)
{
    bool complexArg = false;
    bool isNegativeNum = true;

    if (*arg != '-') return true;

    while (*arg != '\0')
    {
        if(*arg == '-' || *arg == '.' || *arg == ',') 
        {
            ++arg;
            continue;
        }
        if(*arg == ' ') 
        {
            complexArg = true;
            break;
        }

        isNegativeNum &= (isdigit(*arg) != 0);
        ++arg;
    }

    return (complexArg || isNegativeNum);
}

bool _IsOptArgValuable(ScmdpWorkspace* workspace, const char* key)
{
    bool valuable = false;

    for (int i = 0; i < workspace->numOfOptArgs; i++)
    {
        if(strcmp(workspace->optArgs[i].longKey, key) == 0 || strcmp(workspace->optArgs[i].shortKey, key) == 0)
        {
            valuable = workspace->optArgs[i].isValuable;
            break;
        }
    }
    
    return valuable;
}

void _DropValIntoOpArg(ScmdpWorkspace* workspace, const char* key, const char* val)
{
    for (int i = 0; i < workspace->numOfOptArgs; i++)
    {
        if(strcmp(workspace->optArgs[i].longKey, key) == 0 || strcmp(workspace->optArgs[i].shortKey, key) == 0)
        {
            *(workspace->optArgs[i].valPlace) = val;
            return;
        }
    }
}

int _ParseOptArg(ScmdpWorkspace* workspace, int* iterator, const char* arg, int argc, const char *argv[], bool revOrder)
{
    if(!_IsOptArgKeyExists(workspace, arg)) return ERR_UNKNOWN_PARAMETER;

    if(_IsOptArgValuable(workspace, arg))
    {
        /* If you try to sent a non-optional arg value into an optional */
        const bool isNoptArgVal = (revOrder && *iterator+1 >= argc - workspace->numOfNonOptArgs);

        if((*iterator+1 >= argc) || !_IsNotAKey(argv[*iterator+1]) || isNoptArgVal) return ERR_NO_VAL_OPT_PARAMETER;
        else _DropValIntoOpArg(workspace, arg, argv[*iterator+1]);
        ++*iterator;
    }
    else _DropValIntoOpArg(workspace, arg, "true");

    return 0;
}

SCMDPStatus ParseArgs(ScmdpWorkspace *workspace, int argc, const char *argv[])
{
    SCMDPStatus success = SCMDP_GOOD;    

    if (_IsHelpKeyPresents(workspace, argc, argv))
    {
        _ShowHelp(workspace, true);
        _DeleteWorkspace(workspace);
        return SCMDP_HELP;
    }
    /* Analyze if arguments too many or too little */
    if (argc-1 > workspace->numOfNonOptArgs + workspace->numOfOptArgs + workspace->numOfValOptArgs)
    {
        _ShowHelp(workspace, false);
        _DeleteWorkspace(workspace);
        return SCMDP_BAD;
    }
    if (argc-1 < workspace->numOfNonOptArgs)
    {
        _ShowHelp(workspace, false);
        _DeleteWorkspace(workspace);
        return SCMDP_HELP;
    }
    
    /********************* If it all is good lets process our args ********************/

    /* If the first argument is non-optional, we go parse arguments in direct order */
    if(_IsNotAKey(argv[1]))
    {
        for (int i = 1; i < argc; i++)
        {
            if(_IsNotAKey(argv[i]) && (i < workspace->numOfNonOptArgs+1)) 
            {
                /* No special function is needed since non-optional arguments follow in strict order */
                *(workspace->nonOptArgs[i-1].valPlace) = argv[i];
            }
            else if(!_IsNotAKey(argv[i]) && (i >= workspace->numOfNonOptArgs+1))
            {
                const int fail = _ParseOptArg(workspace, &i, argv[i], argc, argv, false);
                
                if(fail > 0)
                {
                    _ShowError(workspace, fail);
                    success = SCMDP_BAD;
                    break;
                } 
            }
            else
            {
                _ShowError(workspace, ERR_UNKNOWN_PARAMETER);
                success = SCMDP_BAD;
                break;
            }
        }
    }
    /* If the first argument is optional, we go parse arguments in direct order too */
    else
    {
        for (int i = 1; i < argc; i++)
        {
            if(_IsNotAKey(argv[i]) && i < argc - workspace->numOfNonOptArgs) 
            {
                _ShowError(workspace, ERR_WRONG_SYNTAX);
                success = SCMDP_BAD;
                break;
            }
            else if(!_IsNotAKey(argv[i]) && (i < argc - workspace->numOfNonOptArgs))
            {
                const int fail = _ParseOptArg(workspace, &i, argv[i], argc, argv, true);

                if(fail > 0)
                {
                    _ShowError(workspace, fail);
                    success = SCMDP_BAD;
                    break;
                } 
            }
            else if(_IsNotAKey(argv[i]) && (i >= argc - workspace->numOfNonOptArgs))
            {
                *(workspace->nonOptArgs[i - (argc - workspace->numOfNonOptArgs)].valPlace) = argv[i];
            }
            else
            {
                _ShowError(workspace, ERR_UNKNOWN_PARAMETER);
                success = SCMDP_BAD;
                break;
            }
        }
    }

    _DeleteWorkspace(workspace);
    return success;
}    

