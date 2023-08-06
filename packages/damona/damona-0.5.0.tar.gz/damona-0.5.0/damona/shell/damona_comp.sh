#version: 0.9.15
function _mycomplete_damona()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="build activate deactivate env install list registry --pattern
--from-url"
    case "${prev}" in
    
            build)
                xpat=".[!.]*"
                COMPREPLY=( $(compgen -X "${xpat}" -d ${cur}) )
                return 0
                ;;
            list)
                local choices="--from-url --pattern"
                COMPREPLY=( $(compgen -W "${choices}" -- ${cur}) )
                return 0
                ;;
        #;;
    esac
    #if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    #fi

}
complete -o  default -F _mycomplete_damona damona
    
