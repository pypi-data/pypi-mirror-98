import React from 'react';
import Pin from '../assets/caption-pin.svg';
import Call from '../assets/caption-call.svg';
import Email from '../assets/caption-email.svg';
import Next from '../assets/next.svg';


function FamilyCard(props) {
    return(
        <div  style={{  }}   className="offer-card">
            <a href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]}
                target="_blank"
                aria-label={props.item["title"]}
                data-check-info-section="true"
                className="gjfol"
            >
            </a>
            <div className="card-container-img">
                <div className="card-ratio">
                    <a className="card-img-link" href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} 
                        target="_blank"
                        aria-hidden="true"
                        aria-label={props.item["title"]}
                        style={{backgroundImage: `url(${"https://pivotweb.tourismewallonie.be/PivotWeb-3.1/img/" + props.item["offer"]["offerID"]})` }}
                        > 
                        {/* <img className="embed-responsive-img offer-card-img" variant="top" src={"https://pivotweb.tourismewallonie.be/PivotWeb-3.1/img/" + props.item["offer"]["offerID"] } /> */}
                    </a>
                </div>
            </div>
            <div className="card-caption">
                <div className='card-caption-title' href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank">{props.item["title"]}</div>
                
                <div className="card-caption-details">
                    {props.item["phone"] ?
                        <span className='card-caption-num'>
                            <img className='card-icon' src={Call} alt="Logo pin" />
                            <a href={"tel:"+props.item["phone"]}>{props.item["phone"]}</a>
                        </span>
                        :""} 

                    {props.item["email"] ?
                        <span className='card-caption-email'>
                            <img className='card-icon' src={Email} alt="Logo pin" />
                            <a href={"mailto:"+props.item["email"]}>{props.item["email"]}</a>
                        </span>
                    :""}
                    {props.item["cp"] ? 
                        <span aria-label="Code postal" className='card-caption-cp'>
                            <img className='card-icon' src={Pin} alt="Logo pin" /> 
                            {props.item["cp"]}
                        </span>
                    :""}
                {/* <span className='card-caption-details'>
                        <a href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank">Détails</a>
                        <img className='card-next' src={Next} alt="Logo pin" /> 
                    </span> */}
                </div>
            </div>
        </div>
    );
}
export default FamilyCard;