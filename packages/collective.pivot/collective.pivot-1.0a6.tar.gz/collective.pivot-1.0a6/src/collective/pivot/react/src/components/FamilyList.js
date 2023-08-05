import React, {useState, useEffect} from 'react';
import FamilyCard from './FamilyCard';

function FamilyList(props) {
    const [state, setState] = useState([]);
    const [infoUrl, setInfoUrl] = useState("");

    useEffect(() => {
        setState(props.items)
        setInfoUrl(props.details)

     }, [props])

     function handleChange(event) {
        props.onChange(event);
    }
    return(
        <ul className="pivot-offer-list-container">
           {state && state.map((item, i) => (<li onMouseEnter={() => handleChange(i)} onMouseLeave={() => handleChange(null)} className="pivot-item">
               <FamilyCard key={i} infoUrl={infoUrl}  item={item}/></li>))}
        </ul>
    );
}

export default FamilyList;